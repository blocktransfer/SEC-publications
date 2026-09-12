#!/usr/bin/env python3

from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import argparse
import hashlib
import time

import img2pdf
from playwright.sync_api import sync_playwright


URL = "https://play.google.com/books/reader?id=DaJvZJZP0ncC"
OUT_DIR = Path("disclosure-corporate-ownership-pages")
OUT_PDF = Path("Disclosure_of_Corporate_Ownership.pdf")
PROFILE = Path(".google-books-browser")

MAX_PAGES = 500
WRITE_WORKERS = 4

# Navigation is intentionally simple: this reader reliably advances with
# ArrowRight. Send exactly one keypress per captured page and observe the
# fixed visible page rectangle before doing anything else.
NAV_CHANGE_TIMEOUT = 12.0
NAV_OBSERVE_ROUNDS = 5
NAV_KEY_ATTEMPTS = 4
RENDER_SETTLE_SECONDS = 1.2
START_JUMP_ATTEMPTS = 6

OUT_DIR.mkdir(exist_ok=True)


FIND_PAGE_CANDIDATE = r"""
() => {
    const vw = window.innerWidth ||
               document.documentElement.clientWidth;
    const vh = window.innerHeight ||
               document.documentElement.clientHeight;

    const candidates = document.querySelectorAll(
        "img, canvas, svg, div, section"
    );

    function isVisual(el) {
        const tag = el.tagName;

        if (
            tag === "IMG" ||
            tag === "CANVAS" ||
            tag === "SVG"
        ) {
            return true;
        }

        const style = getComputedStyle(el);

        return (
            style.backgroundImage &&
            style.backgroundImage !== "none"
        );
    }

    let best = null;

    for (const el of candidates) {
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);

        if (
            style.display === "none" ||
            style.visibility === "hidden" ||
            Number(style.opacity || 1) === 0
        ) {
            continue;
        }

        // Must overlap the current viewport.
        if (
            rect.right <= 0 ||
            rect.bottom <= 0 ||
            rect.left >= vw ||
            rect.top >= vh
        ) {
            continue;
        }

        const visibleWidth =
            Math.min(rect.right, vw) -
            Math.max(rect.left, 0);

        const visibleHeight =
            Math.min(rect.bottom, vh) -
            Math.max(rect.top, 0);

        if (
            visibleWidth < 200 ||
            visibleHeight < 300
        ) {
            continue;
        }

        const ratio = rect.width / rect.height;

        // A scanned book page should be approximately portrait.
        if (ratio < 0.30 || ratio > 1.20) {
            continue;
        }

        const ownVisual = isVisual(el);

        // Google sometimes tiles a page underneath a wrapper.
        let directVisualChild = false;

        for (const child of el.children) {
            if (isVisual(child)) {
                directVisualChild = true;
                break;
            }
        }

        if (!ownVisual && !directVisualChild) {
            continue;
        }

        const area = visibleWidth * visibleHeight;

        // Prefer elements centered in the reader.
        const x =
            rect.left + rect.width / 2;
        const y =
            rect.top + rect.height / 2;

        const dx =
            Math.abs(x - vw / 2) / vw;
        const dy =
            Math.abs(y - vh / 2) / vh;

        const centerBonus =
            1 / (1 + dx * 3 + dy * 2);

        // Ordinary portrait pages get a bonus.
        const portraitBonus =
            ratio >= 0.45 && ratio <= 0.90
                ? 2.0
                : 1.0;

        // Avoid accidentally choosing the entire reader application.
        const fullscreenPenalty =
            rect.width > vw * 0.94 &&
            rect.height > vh * 0.94
                ? 0.05
                : 1.0;

        // Actual page surfaces generally do not contain controls.
        const controls =
            el.querySelectorAll(
                "button, input, [role='button']"
            ).length;

        const controlPenalty =
            controls > 0 ? 0.2 : 1.0;

        const score =
            area *
            centerBonus *
            portraitBonus *
            fullscreenPenalty *
            controlPenalty;

        if (!best || score > best.score) {
            best = {
                el,
                score,
                width: rect.width,
                height: rect.height,
                tag: el.tagName,
                ownVisual,
                directVisualChild
            };
        }
    }

    if (!best) {
        return null;
    }

    const token =
        "gbook-" +
        Math.random().toString(36).slice(2) +
        Date.now().toString(36);

    best.el.setAttribute(
        "data-gbook-capture-target",
        token
    );

    return {
        token,
        score: best.score,
        width: best.width,
        height: best.height,
        tag: best.tag,
        ownVisual: best.ownVisual,
        directVisualChild: best.directVisualChild
    };
}
"""


def find_page_element(page):
    """Return the best page-like element from any frame."""
    best = None

    for frame_number, frame in enumerate(page.frames):
        try:
            candidate = frame.evaluate(FIND_PAGE_CANDIDATE)
        except Exception:
            continue

        if not candidate:
            continue

        candidate["frame_number"] = frame_number
        candidate["frame_url"] = frame.url

        if best is None or candidate["score"] > best["info"]["score"]:
            best = {"frame": frame, "info": candidate}

    if best is None:
        return None, None

    token = best["info"]["token"]
    locator = best["frame"].locator(
        f'[data-gbook-capture-target="{token}"]'
    )
    return locator, best["info"]


def capture_page(page, verbose=False):
    """Capture the currently rendered page element and return its PNG + digest."""
    locator, info = find_page_element(page)

    if locator is None:
        print("\nFrames visible to Playwright:")
        for i, frame in enumerate(page.frames):
            print(f"  [{i}] {frame.url or '(no URL)'}")
        raise RuntimeError(
            "Could not locate the rendered Google Books page in any frame."
        )

    locator.wait_for(state="visible", timeout=5000)
    box = locator.bounding_box()
    png = locator.screenshot(
        type="png",
        animations="disabled",
        caret="hide",
    )
    tag = locator.evaluate("(el) => el.tagName")
    digest = hashlib.sha256(png).hexdigest()

    if verbose:
        print(
            "    detected "
            f"{tag} {info['width']:.0f}×{info['height']:.0f} "
            f"in frame {info['frame_number']}"
        )

    return png, digest, tag, box


def _clamp_clip_to_viewport(page, box):
    """Clamp a page bounding box to the visible top-level viewport."""
    if not box:
        return None

    viewport = page.viewport_size or {"width": 1800, "height": 2200}
    vw = float(viewport["width"])
    vh = float(viewport["height"])

    x = max(0.0, float(box["x"]))
    y = max(0.0, float(box["y"]))
    right = min(vw, float(box["x"]) + float(box["width"]))
    bottom = min(vh, float(box["y"]) + float(box["height"]))

    width = right - x
    height = bottom - y

    if width < 50 or height < 50:
        return None

    # Stay a pixel inside the viewport to avoid Playwright clip rounding errors.
    return {
        "x": x,
        "y": y,
        "width": max(1.0, width - 1.0),
        "height": max(1.0, height - 1.0),
    }


def visible_page_digest(page, box):
    """Hash the pixels visibly occupying the current page rectangle.

    This intentionally screenshots a FIXED viewport rectangle instead of
    re-running find_page_element(). Google may briefly leave the old page in the
    DOM during a turn, which made the old detector follow a stale element even
    though the reader visibly advanced.
    """
    clip = _clamp_clip_to_viewport(page, box)
    if clip is None:
        return None

    png = page.screenshot(
        type="png",
        clip=clip,
        animations="disabled",
        caret="hide",
    )
    return hashlib.sha256(png).hexdigest()


def _parse_int(text):
    if text is None:
        return None
    text = str(text).strip().replace(",", "")
    if text.isdigit():
        return int(text)
    return None


def page_number_controls(page):
    """Yield visible controls that look like Google Books page-number inputs."""
    selectors = [
        'input[aria-label*="page" i]',
        'input[title*="page" i]',
        'input[placeholder*="page" i]',
        '[contenteditable="true"][aria-label*="page" i]',
        '[contenteditable="true"][title*="page" i]',
    ]

    seen = set()
    for frame in page.frames:
        for selector in selectors:
            try:
                loc = frame.locator(selector)
                count = loc.count()
            except Exception:
                continue

            for i in range(count):
                item = loc.nth(i)
                try:
                    if not item.is_visible():
                        continue
                    key = (frame.url, selector, i)
                    if key in seen:
                        continue
                    seen.add(key)
                    yield item
                except Exception:
                    continue


def read_reader_page_number(page):
    """Best-effort read of the visible reader page-number control."""
    for control in page_number_controls(page):
        try:
            tag = control.evaluate('(el) => el.tagName')
            if tag == 'INPUT':
                value = control.input_value()
            else:
                value = control.text_content()
            number = _parse_int(value)
            if number is not None:
                return number
        except Exception:
            continue
    return None


def jump_to_reader_page(page, target, attempts=START_JUMP_ATTEMPTS):
    """Automatically move Google Play Books to a requested reader page.

    This only uses a visible page-number control. It does not guess by firing a
    large number of ArrowRight events, so restarting cannot accidentally skip
    through the book.
    """
    if target < 1:
        raise ValueError("Reader page must be positive")
    if read_reader_page_number(page) == target:
        return True

    for attempt in range(1, attempts + 1):
        controls = list(page_number_controls(page))
        if not controls:
            print(f"    restart jump attempt {attempt}/{attempts}: page box not found")
            time.sleep(1.0)
            continue

        for control in controls:
            try:
                _, old_digest, _, old_box = capture_page(page)
                old_visual = visible_page_digest(page, old_box)
                control.click(force=True)

                control.fill(str(target))

                control.press('Enter')
                print(
                    f"    restart jump attempt {attempt}/{attempts}: "
                    f"requested reader page {target}"
                )

                # A typed value is not confirmation: require a settled page
                # image as well as the requested reader number after submission.
                changed, _ = wait_for_page_change_once(
                    page, old_box, old_visual, old_digest, None,
                    timeout=NAV_CHANGE_TIMEOUT,
                )
                if changed and read_reader_page_number(page) == target:
                    blur_reader_focus(page)
                    return True

            except Exception:
                continue

        time.sleep(1.0)

    return False


def wait_for_page_change_once(
    page,
    old_box,
    old_visual_digest,
    old_page_digest,
    old_reader_number,
    timeout=NAV_CHANGE_TIMEOUT,
):
    """Wait for changed page pixels to remain stable through rendering.

    A counter can update before the image. It is supporting evidence only;
    capturing immediately on a counter change can save the previous page.
    """
    deadline = time.monotonic() + timeout
    stable_digest = None
    stable_since = None

    while time.monotonic() < deadline:
        try:
            visual = visible_page_digest(page, old_box)
            _, digest, _, _ = capture_page(page, verbose=False)
            current = read_reader_page_number(page)
            changed = (
                digest != old_page_digest
                and visual is not None
                and (old_visual_digest is None or visual != old_visual_digest)
            )
            counter_ready = (
                old_reader_number is None
                or current is None
                or current != old_reader_number
            )
            if changed and counter_ready:
                if digest != stable_digest:
                    stable_digest = digest
                    stable_since = time.monotonic()
                elif time.monotonic() - stable_since >= RENDER_SETTLE_SECONDS:
                    return True, "settled page image"
            else:
                stable_digest = stable_since = None
        except Exception:
            stable_digest = stable_since = None

        time.sleep(0.30)

    return False, None


def blur_reader_focus(page):
    """Blur text-entry controls so ArrowRight reaches the reader."""
    for frame in page.frames:
        try:
            frame.evaluate(
                """() => {
                    const el = document.activeElement;
                    if (el && el.blur) el.blur();
                }"""
            )
        except Exception:
            pass


def advance_page(page, old_box, old_page_digest):
    """Advance one page, with many checks but no blind double-skip retries.

    The first ArrowRight is always sent. We then run several observation rounds.
    Another ArrowRight is sent only if a readable page-number field positively
    confirms that the reader is STILL on the old page.
    """
    blur_reader_focus(page)
    old_visual_digest = visible_page_digest(page, old_box)
    if old_visual_digest is None:
        print("    could not establish the visible page rectangle")
        return False

    old_reader_number = read_reader_page_number(page)

    for key_attempt in range(1, NAV_KEY_ATTEMPTS + 1):
        blur_reader_focus(page)

        try:
            page.keyboard.press("ArrowRight")
        except Exception as exc:
            print(f"    ArrowRight failed to send: {exc}")
            return False

        print(
            f"    ArrowRight attempt {key_attempt}/{NAV_KEY_ATTEMPTS}; "
            f"checking for the new page..."
        )

        for observe_round in range(1, NAV_OBSERVE_ROUNDS + 1):
            changed, reason = wait_for_page_change_once(
                page,
                old_box,
                old_visual_digest,
                old_page_digest,
                old_reader_number,
                timeout=NAV_CHANGE_TIMEOUT,
            )
            if changed:
                print(
                    f"    advanced with ArrowRight "
                    f"(confirmed by {reason}, check {observe_round}/{NAV_OBSERVE_ROUNDS})"
                )
                return True

            print(
                f"    no change confirmed yet "
                f"(check {observe_round}/{NAV_OBSERVE_ROUNDS})"
            )

        # Never blindly press ArrowRight again. Only retry the key if Google's
        # own readable page counter proves that we are still on the same page.
        if old_reader_number is None:
            print(
                "    could not safely verify the reader stayed on the old page; "
                "not sending another ArrowRight"
            )
            return False

        current = read_reader_page_number(page)
        if current is None:
            print(
                "    page counter became unreadable; not sending another "
                "ArrowRight because that could skip a page"
            )
            return False

        if current != old_reader_number:
            print(
                f"    reader counter moved from {old_reader_number} to {current}; "
                "but the new image did not settle; stopping capture"
            )
            return False

        if key_attempt < NAV_KEY_ATTEMPTS:
            print(
                f"    reader counter still says {current}; safe to retry ArrowRight"
            )
            time.sleep(0.75)

    print(
        f"    reader counter stayed at {old_reader_number} after "
        f"{NAV_KEY_ATTEMPTS} ArrowRight attempts"
    )
    return False

def write_png(path, data):
    path.write_bytes(data)
    return path


def existing_page_images():
    """Return existing PNGs in filename order.

    Resume numbering deliberately uses the *count* of PNG files, matching the
    original script's logic: len(existing) + 1.
    """
    return sorted(OUT_DIR.glob("*.png"))


def numbered_existing_pages():
    """Return numeric PNG filenames in numeric order for PDF assembly."""
    pages = []
    for path in OUT_DIR.glob("*.png"):
        try:
            number = int(path.stem)
        except ValueError:
            continue
        pages.append((number, path))
    return sorted(pages)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Capture accessible Google Play Books pages into a PDF."
    )
    parser.add_argument(
        "--start",
        type=int,
        default=None,
        help=(
            "Output/capture number to start at. If omitted, use the original "
            "resume logic: number of existing PNGs + 1."
        ),
    )
    parser.add_argument(
        "--reader-page",
        type=int,
        default=None,
        help=(
            "Google Play Books reader page to jump to on startup. If omitted, "
            "use the same number as the resume/output start page."
        ),
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=MAX_PAGES,
        help="Highest output page number to capture.",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=WRITE_WORKERS,
        help="Background image-write threads (browser automation stays serial).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    existing = existing_page_images()

    if args.start is not None:
        start_number = max(1, args.start)
    else:
        start_number = len(existing) + 1

    if existing:
        print(
            f"Found {len(existing)} existing PNG(s) in {OUT_DIR}; "
            f"capture numbering starts at {start_number}."
        )

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            str(PROFILE),
            headless=False,
            viewport={"width": 1800, "height": 2200},
            device_scale_factor=2,
        )

        pages = context.pages
        page = pages[0] if pages else context.new_page()

        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000,
        )

        time.sleep(2)

        reader_page = (
            max(1, args.reader_page)
            if args.reader_page is not None
            else start_number
        )

        print()
        print("Google Play Books is open.")
        print("Use SINGLE-PAGE mode and make sure no menu covers the page.")
        print(
            f"The first captured file will be "
            f"{OUT_DIR / f'{start_number:04d}.png'}"
        )

        if reader_page >= 1:
            print(f"Automatically jumping to reader page {reader_page}...")
            if jump_to_reader_page(page, reader_page):
                print(f"Reader positioned at page {reader_page}.")
            else:
                print(
                    f"Could not automatically confirm reader page {reader_page}. "
                    "Position it manually before continuing."
                )

        input("Press Enter when ready to start capture... ")

        seen = set()
        # Include existing hashes so a resumed run can detect accidental overlap.
        for path in existing:
            try:
                seen.add(hashlib.sha256(path.read_bytes()).hexdigest())
            except Exception:
                pass

        pending_writes = []

        with ThreadPoolExecutor(
            max_workers=max(1, args.workers),
            thread_name_prefix="page-writer",
        ) as pool:
            n = start_number
            while n <= args.max_pages:
                png, digest, tag, box = capture_page(page, verbose=False)

                if digest in seen:
                    print(
                        f"{n:04d}: current reader page was already captured; "
                        "advancing without consuming an output number."
                    )
                    if not advance_page(page, box, digest):
                        print()
                        print(
                            "Could not advance past the duplicate page. "
                            "Stopping without renumbering later pages."
                        )
                        break
                    continue

                filename = OUT_DIR / f"{n:04d}.png"
                pending_writes.append(
                    pool.submit(write_png, filename, png)
                )
                seen.add(digest)

                if box:
                    print(
                        f"{n:04d}: {tag} "
                        f"{box['width']:.0f}×{box['height']:.0f} "
                        f"→ {filename}"
                    )
                else:
                    print(f"{n:04d}: → {filename}")

                if n >= args.max_pages:
                    break

                if not advance_page(page, box, digest):
                    print()
                    print(
                        f"Could not advance after capture {n}. "
                        "Stopping without assuming that this is the book's end."
                    )
                    break

                n += 1

            # Surface any background disk-write exception before PDF creation.
            for future in pending_writes:
                future.result()

        context.close()

    all_pages = [p for _, p in numbered_existing_pages()]
    if not all_pages:
        raise RuntimeError("No page images were saved.")

    print(f"\nCombining {len(all_pages)} pages...")
    with OUT_PDF.open("wb") as f:
        f.write(img2pdf.convert([str(x) for x in all_pages]))

    print(f"Created: {OUT_PDF}")
    print(f"Pages:   {len(all_pages)}")


if __name__ == "__main__":
    main()

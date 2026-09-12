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
# ArrowRight. Retry the same known-good action instead of guessing at buttons,
# page fields, or alternate shortcuts.
NAV_CHANGE_TIMEOUT = 8.0
NAV_RETRIES = 5
RENDER_SETTLE_SECONDS = 0.7

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


def wait_for_page_change(page, old_digest, timeout=NAV_CHANGE_TIMEOUT):
    """
    Wait only until the rendered page differs from old_digest.

    The previous version demanded several identical screenshots after the page
    changed. That made every page appear to be read repeatedly and slowed
    navigation considerably.
    """
    deadline = time.monotonic() + timeout

    while time.monotonic() < deadline:
        try:
            _, digest, _, _ = capture_page(page, verbose=False)
        except Exception:
            time.sleep(0.20)
            continue

        if digest != old_digest:
            time.sleep(RENDER_SETTLE_SECONDS)
            return True

        time.sleep(0.35)

    return False


def focus_reader(page):
    """Remove focus from text fields and click the rendered page."""
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

    locator, _ = find_page_element(page)
    if locator is not None:
        try:
            locator.click(position={"x": 20, "y": 20}, force=True)
        except Exception:
            pass


def advance_page(page, old_digest):
    """Advance exactly one page using ArrowRight.

    ArrowRight is the known-good control for this Google Play Books reader.
    If Google drops focus or is still loading, refocus the rendered page and
    retry the same key instead of switching to unrelated shortcuts.
    """
    for attempt in range(1, NAV_RETRIES + 1):
        focus_reader(page)

        try:
            page.keyboard.press("ArrowRight")
        except Exception as exc:
            print(f"    ArrowRight failed to send: {exc}")
            time.sleep(0.5)
            continue

        if wait_for_page_change(
            page, old_digest, timeout=NAV_CHANGE_TIMEOUT
        ):
            print(f"    advanced with ArrowRight (attempt {attempt})")
            return True

        print(
            f"    no page change after ArrowRight "
            f"(attempt {attempt}/{NAV_RETRIES})"
        )
        time.sleep(0.75)

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

        print()
        print("Google Play Books is open.")
        print("Use SINGLE-PAGE mode and make sure no menu covers the page.")
        print(
            f"The first captured file will be "
            f"{OUT_DIR / f'{start_number:04d}.png'}"
        )
        input("Press Enter when the reader is on the correct starting page... ")

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
                    if not advance_page(page, digest):
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

                if not advance_page(page, digest):
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

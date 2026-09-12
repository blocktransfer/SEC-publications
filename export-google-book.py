#!/usr/bin/env python3

from pathlib import Path
import hashlib
import time
import img2pdf
from playwright.sync_api import sync_playwright

URL = "https://play.google.com/books/reader?id=DaJvZJZP0ncC"

OUT_DIR = Path("disclosure-corporate-ownership-pages")
OUT_PDF = Path("Disclosure_of_Corporate_Ownership.pdf")
PROFILE = Path(".google-books-browser")

MAX_PAGES = 500

OUT_DIR.mkdir(exist_ok=True)

# Google Play Books may render an Original Pages scan inside a nested frame
# and may compose one page from multiple image/canvas/background-image tiles.
# Search every frame and select the most page-like rendered surface.

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
    """
    Search the main document AND every nested iframe for the
    most page-like rendered element.
    """

    best = None

    for frame_number, frame in enumerate(page.frames):
        try:
            candidate = frame.evaluate(
                FIND_PAGE_CANDIDATE
            )
        except Exception:
            # Cross-origin frames are normally accessible through
            # Playwright, but ignore any frame that cannot execute.
            continue

        if not candidate:
            continue

        candidate["frame_number"] = frame_number
        candidate["frame_url"] = frame.url

        if (
            best is None or
            candidate["score"] > best["info"]["score"]
        ):
            best = {
                "frame": frame,
                "info": candidate,
            }

    if best is None:
        return None, None

    token = best["info"]["token"]

    locator = best["frame"].locator(
        f'[data-gbook-capture-target="{token}"]'
    )

    return locator, best["info"]


def capture_page(page):
    locator, info = find_page_element(page)

    if locator is None:
        print()
        print("Frames visible to Playwright:")

        for i, frame in enumerate(page.frames):
            print(
                f"  [{i}] "
                f"{frame.url or '(no URL)'}"
            )

        raise RuntimeError(
            "Could not locate the rendered Google Books page "
            "in any frame."
        )

    try:
        locator.wait_for(
            state="visible",
            timeout=5000,
        )

        box = locator.bounding_box()

        png = locator.screenshot(
            type="png",
            animations="disabled",
            caret="hide",
        )

        tag = locator.evaluate(
            "(el) => el.tagName"
        )

    except Exception as exc:
        raise RuntimeError(
            f"Found a candidate page but could not capture it: {exc}"
        )

    digest = hashlib.sha256(png).hexdigest()

    # Useful while we're figuring out Google's renderer.
    print(
        "    detected "
        f"{tag} "
        f"{info['width']:.0f}×{info['height']:.0f} "
        f"in frame {info['frame_number']}"
    )

    return png, digest, tag, box


def wait_for_next_page(page, old_digest, timeout=15):
    """
    Wait until:
      1. the rendered page changes; and
      2. the new page remains identical across successive captures.

    This avoids saving an intermediate page-turn/loading frame.
    """

    deadline = time.time() + timeout
    changed = False
    previous = None
    stable_count = 0

    while time.time() < deadline:
        try:
            png, digest, tag, box = capture_page(page)
        except Exception:
            time.sleep(0.25)
            continue

        if digest != old_digest:
            changed = True

        if changed:
            if digest == previous:
                stable_count += 1
            else:
                previous = digest
                stable_count = 0

            if stable_count >= 2:
                return True

        time.sleep(0.3)

    return False


def main():
    files = []

    with sync_playwright() as p:
        context = p.chromium.launch_persistent_context(
            str(PROFILE),
            headless=False,

            # Large virtual viewport makes Google request/render
            # a relatively high-resolution page.
            viewport={
                "width": 1800,
                "height": 2200,
            },

            device_scale_factor=2,
        )

        pages = context.pages
        page = pages[0] if pages else context.new_page()

        page.goto(
            URL,
            wait_until="domcontentloaded",
            timeout=60000,
        )

        print()
        print("Google Play Books is open.")
        print()
        print("Before continuing:")
        print("  1. Put the reader in SINGLE-PAGE mode.")
        print("  2. Go to the very first page/cover.")
        print("  3. Make sure no menu is covering the page.")
        print()

        input("Press Enter here when ready... ")

        seen = set()

        for n in range(1, MAX_PAGES + 1):
            png, digest, tag, box = capture_page(page)

            # Avoid accidentally writing duplicate pages.
            if digest in seen:
                print(
                    f"Duplicate image encountered at {n}; "
                    "trying to advance..."
                )
            else:
                filename = OUT_DIR / f"{n:04d}.png"
                filename.write_bytes(png)

                files.append(filename)
                seen.add(digest)

                if box:
                    print(
                        f"{n:04d}: {tag} "
                        f"{box['width']:.0f}×{box['height']:.0f} "
                        f"→ {filename}"
                    )
                else:
                    print(f"{n:04d}: → {filename}")

            # Remove focus from any page-number/search field.
            page.evaluate("""
                () => {
                    if (document.activeElement) {
                        document.activeElement.blur();
                    }
                }
            """)

            def advance_page(page, old_digest):
                """
                Advance Google Play Books by focusing the actual reader first.
                Try Google's supported shortcuts, then its visible next button.
                """

                # First focus the actual rendered book page, including if it lives
                # inside an iframe.
                locator, info = find_page_element(page)

                if locator is not None:
                    try:
                        locator.focus()
                    except Exception:
                        try:
                            locator.click(
                                position={"x": 10, "y": 10},
                                force=True,
                            )
                        except Exception:
                            pass

                # Google documents all four of these as "next page".
                for key in ("n", "j", "ArrowRight", "PageUp"):
                    try:
                        page.keyboard.press(key)

                        if wait_for_next_page(
                            page,
                            old_digest,
                            timeout=3,
                        ):
                            print(f"    advanced with {key}")
                            return True

                    except Exception:
                        pass

                # If keyboard navigation doesn't reach the reader,
                # find Google's visible next-page control in any frame.
                selectors = [
                    '[aria-label*="Next" i]',
                    '[aria-label*="next page" i]',
                    '[title*="Next" i]',
                    '[title*="next page" i]',
                ]

                for frame in page.frames:
                    for selector in selectors:
                        try:
                            buttons = frame.locator(selector)

                            for i in range(buttons.count()):
                                button = buttons.nth(i)

                                if not button.is_visible():
                                    continue

                                button.click(force=True)

                                if wait_for_next_page(
                                    page,
                                    old_digest,
                                    timeout=5,
                                ):
                                    print(
                                        "    advanced with next-page button"
                                    )
                                    return True

                        except Exception:
                            continue

                return False
            if not advance_page(page, digest):
                print()
                print("Could not advance to the next page.")
                break
        context.close()

    if not files:
        raise RuntimeError("No page images were saved.")

    print()
    print(f"Combining {len(files)} pages...")

    with OUT_PDF.open("wb") as f:
        f.write(
            img2pdf.convert(
                [str(x) for x in files]
            )
        )

    print()
    print(f"Created: {OUT_PDF}")
    print(f"Pages:   {len(files)}")


if __name__ == "__main__":
    main()

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

# Google Play Books can render scans as <img>, <canvas>,
# or elements carrying a CSS background image. Find the largest
# visible portrait-shaped candidate.
FIND_PAGE = r"""
() => {
    const candidates = [
        ...document.querySelectorAll("img"),
        ...document.querySelectorAll("canvas"),
        ...document.querySelectorAll("div")
    ];

    let best = null;

    for (const el of candidates) {
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);

        if (rect.width < 300 || rect.height < 400)
            continue;

        if (
            style.display === "none" ||
            style.visibility === "hidden" ||
            parseFloat(style.opacity || "1") === 0
        )
            continue;

        if (el.tagName === "DIV") {
            if (!style.backgroundImage ||
                style.backgroundImage === "none")
                continue;
        }

        const ratio = rect.width / rect.height;

        // Allow ordinary portrait book pages.
        if (ratio < 0.35 || ratio > 1.10)
            continue;

        const area = rect.width * rect.height;

        // Favor portrait-looking elements.
        const score = area * (ratio < 0.9 ? 2 : 1);

        if (!best || score > best.score) {
            best = {
                el: el,
                score: score
            };
        }
    }

    return best ? best.el : null;
}
"""


def capture_page(page):
    handle = page.evaluate_handle(FIND_PAGE)
    element = handle.as_element()

    if element is None:
        handle.dispose()
        raise RuntimeError(
            "Could not find the rendered book page."
        )

    box = element.bounding_box()

    png = element.screenshot(
        type="png",
        animations="disabled",
        caret="hide",
    )

    tag = element.evaluate("el => el.tagName")
    handle.dispose()

    digest = hashlib.sha256(png).hexdigest()

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

            # Google Play Books responds to the right-arrow key.
            page.keyboard.press("ArrowRight")

            if not wait_for_next_page(page, digest):
                print()
                print("Page did not change.")
                print("Assuming the end of the book.")
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

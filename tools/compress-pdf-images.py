#!/usr/bin/env python3
"""Create a smaller OCR PDF by replacing scan images with grayscale JPEGs."""

from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path

import pikepdf
from PIL import Image
from pikepdf import Name


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--quality", type=int, default=45, choices=range(20, 96))
    parser.add_argument("--report", type=Path)
    parser.add_argument(
        "--reported-output",
        type=Path,
        help="final derivative path to record when OUTPUT is an intermediate file",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report_path = args.report or args.output.with_suffix(".compression.json")
    if not args.input.is_file():
        print(f"Input PDF not found: {args.input}", file=sys.stderr)
        return 1
    if args.input.resolve() == args.output.resolve():
        print("Input and output must be different files.", file=sys.stderr)
        return 1
    if args.output.exists() or report_path.exists():
        print("Refusing to overwrite output or report.", file=sys.stderr)
        return 1

    before_size = args.input.stat().st_size
    images_seen = 0
    images_replaced = 0
    encoded_before = 0
    encoded_after = 0

    with pikepdf.open(args.input) as pdf:
        page_count = len(pdf.pages)
        seen_objects: set[tuple[int, int]] = set()
        for page in pdf.pages:
            for image_object in page.Resources.get("/XObject", {}).values():
                if image_object.get("/Subtype") != Name("/Image"):
                    continue
                identity = tuple(image_object.objgen)
                if identity in seen_objects:
                    continue
                seen_objects.add(identity)
                images_seen += 1
                old_data = image_object.read_raw_bytes()
                encoded_before += len(old_data)
                try:
                    image = pikepdf.PdfImage(image_object).as_pil_image().convert("L")
                except Exception as error:
                    print(f"Skipping unsupported image {identity}: {error}", file=sys.stderr)
                    encoded_after += len(old_data)
                    continue

                buffer = io.BytesIO()
                image.save(
                    buffer,
                    format="JPEG",
                    quality=args.quality,
                    optimize=True,
                    progressive=False,
                )
                new_data = buffer.getvalue()
                if len(new_data) >= len(old_data) * 0.95:
                    encoded_after += len(old_data)
                    continue

                for key in ("/Decode", "/DecodeParms", "/Mask", "/SMask"):
                    if key in image_object:
                        del image_object[key]
                image_object.write(new_data, filter=Name("/DCTDecode"))
                image_object["/ColorSpace"] = Name("/DeviceGray")
                image_object["/BitsPerComponent"] = 8
                encoded_after += len(new_data)
                images_replaced += 1

        pdf.save(args.output)

    after_size = args.output.stat().st_size
    with pikepdf.open(args.output) as check:
        if len(check.pages) != page_count:
            raise ValueError("page count changed during compression")

    report = {
        "input": str(args.input),
        "output": str(args.reported_output or args.output),
        "jpeg_quality": args.quality,
        "pages": page_count,
        "images_seen": images_seen,
        "images_replaced": images_replaced,
        "input_bytes": before_size,
        "compressed_image_pdf_bytes": after_size,
        "image_compression_saved_bytes": before_size - after_size,
        "image_compression_reduction_percent": round(
            (1 - after_size / before_size) * 100, 2
        ),
        "encoded_image_bytes_before": encoded_before,
        "encoded_image_bytes_after": encoded_after,
    }
    report_path.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Created compressed PDF: {args.output}")
    print(f"Created compression report: {report_path}")
    print(f"Replaced images: {images_replaced}/{images_seen}")
    print(f"Image-compression reduction: {report['image_compression_reduction_percent']}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

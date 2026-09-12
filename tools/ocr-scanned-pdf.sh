#!/usr/bin/env bash

set -euo pipefail

usage() {
    cat <<'EOF'
Usage: tools/ocr-scanned-pdf.sh INPUT.pdf [OUTPUT.pdf]

Create a searchable PDF from an English-language scanned PDF. If OUTPUT.pdf is
omitted, the output is written beside the input as INPUT-enhanced-ocr.pdf. A
plain-text sidecar is written beside the output for searching and OCR review.

Install the required tools on macOS with:
  brew install ocrmypdf
EOF
}

if [[ $# -lt 1 || $# -gt 2 ]]; then
    usage >&2
    exit 2
fi

input=$1

if [[ ! -f "$input" ]]; then
    printf 'Input PDF not found: %s\n' "$input" >&2
    exit 1
fi

input_dir=$(dirname -- "$input")
input_name=$(basename -- "$input")
input_stem=${input_name%.*}
output=${2:-"$input_dir/$input_stem-enhanced-ocr.pdf"}
output_stem=${output%.*}
sidecar="$output_stem.txt"

if [[ "$input" == "$output" ]]; then
    printf 'Input and output must be different files.\n' >&2
    exit 1
fi

for path in "$output" "$sidecar"; do
    if [[ -e "$path" ]]; then
        printf 'Refusing to overwrite existing file: %s\n' "$path" >&2
        exit 1
    fi
done

for command_name in ocrmypdf qpdf; do
    if ! command -v "$command_name" >/dev/null 2>&1; then
        printf 'Required command not found: %s\n' "$command_name" >&2
        printf 'Install the OCR tools with: brew install ocrmypdf\n' >&2
        exit 1
    fi
done

input_pages=$(qpdf --show-npages "$input")

# Adaptive Otsu thresholding recovered more faint and broken text in this
# archive's old Google Books scans than the default thresholding pass. OCR is
# rendered at 300 DPI, while the source page images remain unchanged in the
# output. Optimization is disabled to avoid lossy image recompression.
ocrmypdf \
    --language eng \
    --output-type pdf \
    --optimize 0 \
    --oversample 300 \
    --tesseract-thresholding adaptive-otsu \
    --no-tesseract-downsample-large-images \
    --sidecar "$sidecar" \
    --no-overwrite \
    "$input" \
    "$output"

qpdf --check "$output"
output_pages=$(qpdf --show-npages "$output")

if [[ "$input_pages" != "$output_pages" ]]; then
    printf 'Page-count mismatch: input=%s output=%s\n' \
        "$input_pages" "$output_pages" >&2
    exit 1
fi

word_count=$(wc -w < "$sidecar" | tr -d ' ')

printf 'Created searchable PDF: %s\n' "$output"
printf 'Created OCR text sidecar: %s\n' "$sidecar"
printf 'Verified pages: %s\n' "$output_pages"
printf 'Recognized word tokens: %s\n' "$word_count"
printf '%s\n' \
    'OCR remains an unverified aid; confirm names, numbers, and tables against the scan.'

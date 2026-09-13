# OCR and tagged PDF workflow

These tools are intended to move to the planned PDF-tooling repository. They
currently live here so the 1974 disclosure scan can be processed reproducibly.

## Create searchable OCR

Run the OCR, paragraph grouping, table-block classification, and heading
tagging without replacing the source:

```sh
tools/ocr-scanned-pdf.sh SOURCE.pdf NEW-OCR.pdf
```

The command refuses to overwrite files. It writes a searchable PDF, a text
sidecar, and a JSON report containing every classified block. Body paragraphs
use `P`, document parts/chapters/appendices use `H1`, sections use `H2`, and
table-like regions use `Div` so table labels are not promoted to headings.

## Create a much smaller derivative

Create a new grayscale JPEG derivative at the tested quality of 45, then apply
the same structure tags:

```sh
tools/compress-and-tag-ocr-pdf.sh EXISTING-OCR.pdf NEW-COMPACT.pdf 45
```

The source is never edited. A compression report records byte counts and the
tagging report records block decisions. Lower JPEG quality is smaller but makes
the scan less useful as visual evidence.

## Set up and run the local AI review

Install the two Ollama models selected for a 48 GB Apple Silicon Mac:

```sh
tools/setup-ollama-ocr.sh
```

Setup also creates `sec-ocr-review`, a local custom model that embeds the
evidence-preservation rules without copying the underlying 32B weights.

Review all page images and initial blocks. The output is JSONL so an interrupted
long run can resume without losing completed pages:

```sh
tools/ollama-review-ocr.py \
  INITIAL-TAGGED.pdf \
  INITIAL-TAGGED.tagging.json \
  REVIEW-v1.jsonl
```

Resume an interrupted review with `--resume`. Test a page range first with
`--pages 45-50`.

Apply the review while creating another new compressed version:

```sh
tools/compress-and-tag-ocr-pdf.sh \
  EXISTING-UNTAGGED-OCR.pdf \
  NEW-AI-REVIEWED-COMPACT.pdf \
  45 \
  REVIEW-v1.jsonl
```

The AI prompt treats names, initials, corporate names, dates, references,
quantities, currency, percentages, and table values as protected evidence. A
changed protected token is rejected unless the review supplies image-specific
evidence at confidence 0.98 or higher. The scan remains authoritative.

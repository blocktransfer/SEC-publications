#!/usr/bin/env python3
"""Add heuristic paragraph and heading structure to an OCRmyPDF PDF.

This targets OCRmyPDF's fpdf2 renderer, which places invisible OCR text in one
Form XObject per page and normally emits one BT/ET text object per visual line.
The script groups those lines into paragraphs, labels likely section headings,
and builds the PDF structure and parent trees needed for real tagged content.
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pikepdf
from pikepdf import Array, Dictionary, Name, Operator, String


HEADING_PREFIX = re.compile(
    r"^(?:chapter|part|section|appendix|title)\b", re.IGNORECASE
)
LETTERED_HEADING = re.compile(r"^[A-Z0-9]{1,4}[.)]\s+[A-Z]")
PAGE_NUMBER = re.compile(r"^(?:[ivxlcdm]+|\d+[a-z]?)$", re.IGNORECASE)
GOOGLE_FOOTER = re.compile(r"^digitized\s+by\s+google$", re.IGNORECASE)
WORD_END = re.compile(r"[.!?][\"'’”)]*$")


@dataclass
class OcrLine:
    start: int
    end: int
    text: str
    x: float
    y: float
    size: float
    artifact: bool = False
    heading: str | None = None


@dataclass
class LogicalBlock:
    start: int
    end: int
    text: str
    tag: str | None
    lines: list[OcrLine]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Tag OCR text as paragraphs and section headings."
    )
    parser.add_argument("input", type=Path, help="OCRmyPDF-generated input PDF")
    parser.add_argument("output", type=Path, help="new tagged PDF")
    parser.add_argument(
        "--report",
        type=Path,
        help="optional JSON report (default: OUTPUT.tagging.json)",
    )
    return parser.parse_args()


def unicode_map(font: pikepdf.Object) -> dict[bytes, str]:
    stream = font.get("/ToUnicode")
    if stream is None:
        raise ValueError("OCR font has no /ToUnicode map")
    pairs = re.findall(
        rb"<([0-9A-Fa-f]+)>\s*<([0-9A-Fa-f]+)>", stream.read_bytes()
    )
    result: dict[bytes, str] = {}
    for source, target in pairs:
        try:
            result[bytes.fromhex(source.decode())] = bytes.fromhex(
                target.decode()
            ).decode("utf-16-be")
        except (UnicodeDecodeError, ValueError):
            continue
    return result


def decode_pdf_string(value: pikepdf.Object, mapping: dict[bytes, str]) -> str:
    raw = bytes(value)
    widths = sorted({len(key) for key in mapping}, reverse=True)
    output: list[str] = []
    offset = 0
    while offset < len(raw):
        for width in widths:
            token = raw[offset : offset + width]
            if token in mapping:
                output.append(mapping[token])
                offset += width
                break
        else:
            output.append("�")
            offset += widths[-1] if widths else 1
    return "".join(output)


def decode_show_text(
    operands: pikepdf.Object,
    mapping: dict[bytes, str],
) -> str:
    value = operands[0]
    if isinstance(value, pikepdf.Array):
        return "".join(
            decode_pdf_string(item, mapping)
            for item in value
            if isinstance(item, pikepdf.String)
        )
    return decode_pdf_string(value, mapping)


def multiply(
    outer: tuple[float, float, float, float, float, float],
    inner: tuple[float, float, float, float, float, float],
) -> tuple[float, float, float, float, float, float]:
    a, b, c, d, e, f = outer
    g, h, i, j, k, l = inner
    return (
        a * g + c * h,
        b * g + d * h,
        a * i + c * j,
        b * i + d * j,
        a * k + c * l + e,
        b * k + d * l + f,
    )


def transform(
    matrix: tuple[float, float, float, float, float, float], x: float, y: float
) -> tuple[float, float]:
    a, b, c, d, e, f = matrix
    return a * x + c * y + e, b * x + d * y + f


def extract_lines(
    form: pikepdf.Object, instructions: list[pikepdf.ContentStreamInstruction]
) -> list[OcrLine]:
    resources = form.get("/Resources", Dictionary())
    fonts = resources.get("/Font", Dictionary())
    mappings = {str(name): unicode_map(font) for name, font in fonts.items()}
    if not mappings:
        raise ValueError("OCR Form XObject has no fonts")

    identity = (1.0, 0.0, 0.0, 1.0, 0.0, 0.0)
    ctm = identity
    stack: list[tuple[float, float, float, float, float, float]] = []
    current: dict[str, object] | None = None
    current_font = next(iter(mappings))
    lines: list[OcrLine] = []

    for index, instruction in enumerate(instructions):
        operator = str(instruction.operator)
        operands = instruction.operands
        if operator == "q":
            stack.append(ctm)
        elif operator == "Q":
            ctm = stack.pop() if stack else identity
        elif operator == "cm":
            local = tuple(float(value) for value in operands)
            ctm = multiply(ctm, local)  # type: ignore[arg-type]
        elif operator == "BT":
            current = {
                "start": index,
                "text": [],
                "x": 0.0,
                "y": 0.0,
                "size": 0.0,
                "positioned": False,
            }
        elif current is not None and operator in {"Td", "Tm"}:
            if not current["positioned"]:
                if operator == "Td":
                    local_x, local_y = float(operands[0]), float(operands[1])
                else:
                    local_x, local_y = float(operands[4]), float(operands[5])
                current["x"], current["y"] = transform(ctm, local_x, local_y)
                current["positioned"] = True
        elif current is not None and operator == "Tf":
            current_font = str(operands[0])
            current["size"] = float(operands[1])
        elif current is not None and operator in {"Tj", "TJ"}:
            mapping = mappings.get(current_font)
            if mapping is None:
                raise ValueError(f"missing Unicode map for {current_font}")
            current["text"].append(decode_show_text(operands, mapping))
        elif operator == "ET" and current is not None:
            text = "".join(current["text"]).strip()
            if text:
                lines.append(
                    OcrLine(
                        start=int(current["start"]),
                        end=index,
                        text=text,
                        x=float(current["x"]),
                        y=float(current["y"]),
                        size=float(current["size"]),
                    )
                )
            current = None
    return lines


def letter_stats(text: str) -> tuple[int, float]:
    letters = [character for character in text if character.isalpha()]
    if not letters:
        return 0, 0.0
    uppercase = sum(character.isupper() for character in letters)
    return len(letters), uppercase / len(letters)


def classify_lines(lines: list[OcrLine], page_width: float) -> None:
    ordinary_sizes = [line.size for line in lines if 8 <= line.size <= 30]
    median_size = statistics.median(ordinary_sizes) if ordinary_sizes else 12.0

    for index, line in enumerate(lines):
        stripped = line.text.strip()
        letters, uppercase_ratio = letter_stats(stripped)
        words = stripped.split()
        if (
            GOOGLE_FOOTER.fullmatch(stripped)
            or PAGE_NUMBER.fullmatch(stripped)
            or letters < 2
            or (len(stripped) <= 5 and sum(char.isalnum() for char in stripped) <= 2)
        ):
            line.artifact = True
            continue

        strong_prefix = bool(HEADING_PREFIX.match(stripped))
        lettered = bool(LETTERED_HEADING.match(stripped)) and uppercase_ratio >= 0.72
        previous_is_table_title = index > 0 and lines[index - 1].text.lower().startswith(
            "table "
        )
        table_like = (
            stripped.lower().startswith("table ")
            or stripped.count(".") >= 4
            or sum(character.isdigit() for character in stripped) > max(5, letters // 2)
        )
        all_caps = (
            5 <= letters <= 85
            and 1 <= len(words) <= 11
            and uppercase_ratio >= 0.90
            and not WORD_END.search(stripped)
            and not previous_is_table_title
        )
        visually_prominent = (
            line.size >= median_size * 1.32
            and len(words) <= 10
            and len(stripped) <= 100
            and uppercase_ratio >= 0.72
        )

        if not table_like and (strong_prefix or lettered or all_caps or visually_prominent):
            centered = abs(line.x - page_width * 0.25) < page_width * 0.24
            if strong_prefix or (centered and line.size >= median_size * 1.45):
                line.heading = "H1"
            else:
                line.heading = "H2"


def typical_line_gap(lines: list[OcrLine]) -> float:
    gaps: list[float] = []
    for previous, current in zip(lines, lines[1:]):
        gap = previous.y - current.y
        if 3 <= gap <= 80:
            gaps.append(gap)
    return statistics.median(gaps) if gaps else 24.0


def join_lines(lines: Iterable[OcrLine]) -> str:
    output = ""
    for line in lines:
        text = re.sub(r"\s+", " ", line.text).strip()
        if not output:
            output = text
        elif output.endswith("-") and text and text[0].islower():
            output = output[:-1] + text
        else:
            output += " " + text
    return output


def starts_new_paragraph(
    previous: OcrLine,
    current: OcrLine,
    gap: float,
    left_edge: float,
) -> bool:
    vertical_gap = previous.y - current.y
    if current.y > previous.y + gap:
        return True
    if vertical_gap > gap * 1.55:
        return True
    if current.x > left_edge + 30 and WORD_END.search(previous.text):
        return True
    if current.x > previous.x + 45 and WORD_END.search(previous.text):
        return True
    return False


def build_blocks(lines: list[OcrLine]) -> list[LogicalBlock]:
    if not lines:
        return []
    gap = typical_line_gap(lines)
    body_x = [line.x for line in lines if not line.artifact and line.heading is None]
    left_edge = statistics.quantiles(body_x, n=5)[0] if len(body_x) >= 5 else min(body_x, default=0)
    blocks: list[LogicalBlock] = []
    active: list[OcrLine] = []

    def flush() -> None:
        if not active:
            return
        tag = None if active[0].artifact else (active[0].heading or "P")
        blocks.append(
            LogicalBlock(
                start=active[0].start,
                end=active[-1].end,
                text=join_lines(active),
                tag=tag,
                lines=list(active),
            )
        )
        active.clear()

    for line in lines:
        if not active:
            active.append(line)
            continue
        previous = active[-1]
        category_changed = (
            line.artifact != previous.artifact
            or line.heading != previous.heading
            or line.heading is not None
        )
        if category_changed or (
            not line.artifact
            and line.heading is None
            and starts_new_paragraph(previous, line, gap, left_edge)
        ):
            flush()
        active.append(line)
    flush()
    return blocks


def marked_instruction(tag: str, mcid: int, text: str) -> pikepdf.ContentStreamInstruction:
    properties = Dictionary(MCID=mcid, ActualText=String(text))
    return pikepdf.ContentStreamInstruction(
        [Name("/" + tag), properties], Operator("BDC")
    )


def simple_instruction(operator: str, operands: list[pikepdf.Object] | None = None):
    return pikepdf.ContentStreamInstruction(operands or [], Operator(operator))


def rewrite_form(
    form: pikepdf.Object,
    instructions: list[pikepdf.ContentStreamInstruction],
    blocks: list[LogicalBlock],
) -> None:
    openings: dict[int, list[pikepdf.ContentStreamInstruction]] = {}
    closings: dict[int, list[pikepdf.ContentStreamInstruction]] = {}
    mcid = 0
    for block in blocks:
        if block.tag is None:
            opening = simple_instruction("BMC", [Name("/Artifact")])
        else:
            opening = marked_instruction(block.tag, mcid, block.text)
            mcid += 1
        openings.setdefault(block.start, []).append(opening)
        closings.setdefault(block.end, []).append(simple_instruction("EMC"))

    rewritten: list[pikepdf.ContentStreamInstruction] = []
    for index, instruction in enumerate(instructions):
        rewritten.extend(openings.get(index, []))
        rewritten.append(instruction)
        rewritten.extend(closings.get(index, []))
    form.write(pikepdf.unparse_content_stream(rewritten))


def mark_page_images_as_artifacts(pdf: pikepdf.Pdf, page: pikepdf.Page) -> None:
    image_names = {
        str(name)
        for name, xobject in page.obj.get("/Resources", Dictionary())
        .get("/XObject", Dictionary())
        .items()
        if xobject.get("/Subtype") == Name("/Image")
    }
    if not image_names:
        return
    instructions = pikepdf.parse_content_stream(page.obj)
    rewritten: list[pikepdf.ContentStreamInstruction] = []
    changed = False
    for instruction in instructions:
        if (
            str(instruction.operator) == "Do"
            and str(instruction.operands[0]) in image_names
        ):
            rewritten.append(simple_instruction("BMC", [Name("/Artifact")]))
            rewritten.append(instruction)
            rewritten.append(simple_instruction("EMC"))
            changed = True
        else:
            rewritten.append(instruction)
    if changed:
        page.obj["/Contents"] = pdf.make_stream(
            pikepdf.unparse_content_stream(rewritten)
        )


def find_ocr_form(page: pikepdf.Page) -> pikepdf.Object | None:
    xobjects = page.obj.get("/Resources", Dictionary()).get("/XObject", Dictionary())
    forms = [
        item
        for item in xobjects.values()
        if item.get("/Subtype") == Name("/Form") and item.get("/Resources")
    ]
    return forms[0] if forms else None


def tag_pdf(input_path: Path, output_path: Path, report_path: Path) -> dict[str, object]:
    if input_path.resolve() == output_path.resolve():
        raise ValueError("input and output must be different files")
    if output_path.exists() or report_path.exists():
        raise FileExistsError("refusing to overwrite output or report")

    report: dict[str, object] = {
        "input": str(input_path),
        "output": str(output_path),
        "pages": 0,
        "paragraphs": 0,
        "headings": [],
        "artifact_blocks": 0,
    }

    with pikepdf.open(input_path) as pdf:
        structure_root = pdf.make_indirect(Dictionary(Type=Name("/StructTreeRoot")))
        document = pdf.make_indirect(
            Dictionary(Type=Name("/StructElem"), S=Name("/Document"), P=structure_root)
        )
        document["/K"] = Array()
        structure_root["/K"] = Array([document])
        parent_numbers = Array()
        parent_key = 0

        for page_number, page in enumerate(pdf.pages, start=1):
            mark_page_images_as_artifacts(pdf, page)
            form = find_ocr_form(page)
            if form is None:
                continue
            instructions = list(pikepdf.parse_content_stream(form))
            lines = extract_lines(form, instructions)
            bbox = form.get("/BBox", Array([0, 0, 1, 1]))
            page_width = float(bbox[2]) - float(bbox[0])
            classify_lines(lines, page_width)
            blocks = build_blocks(lines)
            rewrite_form(form, instructions, blocks)

            form["/StructParents"] = parent_key
            parents = Array()
            mcid = 0
            for block in blocks:
                if block.tag is None:
                    report["artifact_blocks"] = int(report["artifact_blocks"]) + 1
                    continue
                content_reference = Dictionary(
                    Type=Name("/MCR"), Pg=page.obj, Stm=form, MCID=mcid
                )
                element = pdf.make_indirect(
                    Dictionary(
                        Type=Name("/StructElem"),
                        S=Name("/" + block.tag),
                        P=document,
                        Pg=page.obj,
                        K=content_reference,
                    )
                )
                if block.tag in {"H1", "H2"}:
                    element["/T"] = String(block.text)
                document["/K"].append(element)
                parents.append(element)
                if block.tag == "P":
                    report["paragraphs"] = int(report["paragraphs"]) + 1
                else:
                    report["headings"].append(
                        {"page": page_number, "level": block.tag, "text": block.text}
                    )
                mcid += 1

            parent_numbers.extend([parent_key, pdf.make_indirect(parents)])
            parent_key += 1
            page.obj["/Tabs"] = Name("/S")
            report["pages"] = int(report["pages"]) + 1

        parent_tree = pdf.make_indirect(Dictionary(Nums=parent_numbers))
        structure_root["/ParentTree"] = parent_tree
        structure_root["/ParentTreeNextKey"] = parent_key
        pdf.Root["/StructTreeRoot"] = structure_root
        pdf.Root["/MarkInfo"] = Dictionary(Marked=True)
        pdf.Root["/Lang"] = String("en-US")
        pdf.save(output_path)

    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    return report


def validate_output(path: Path, expected_pages: int) -> None:
    with pikepdf.open(path) as pdf:
        if len(pdf.pages) != expected_pages:
            raise ValueError("tagged PDF page count changed")
        if pdf.Root.get("/StructTreeRoot") is None:
            raise ValueError("tagged PDF has no /StructTreeRoot")
        mark_info = pdf.Root.get("/MarkInfo", Dictionary())
        if not bool(mark_info.get("/Marked", False)):
            raise ValueError("tagged PDF is not marked as tagged")
        parent_tree = pdf.Root.StructTreeRoot.get("/ParentTree")
        if parent_tree is None or not parent_tree.get("/Nums"):
            raise ValueError("tagged PDF has no structure parent tree")


def main() -> int:
    args = parse_args()
    report_path = args.report or args.output.with_suffix(".tagging.json")
    if not args.input.is_file():
        print(f"Input PDF not found: {args.input}", file=sys.stderr)
        return 1
    try:
        with pikepdf.open(args.input) as source:
            expected_pages = len(source.pages)
        report = tag_pdf(args.input, args.output, report_path)
        validate_output(args.output, expected_pages)
    except Exception as error:
        print(f"Tagging failed: {error}", file=sys.stderr)
        return 1

    print(f"Created tagged PDF: {args.output}")
    print(f"Created tagging report: {report_path}")
    print(f"Tagged OCR pages: {report['pages']}")
    print(f"Paragraphs: {report['paragraphs']}")
    print(f"Headings: {len(report['headings'])}")
    print("Heading detection is heuristic; review the JSON report against the scan.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

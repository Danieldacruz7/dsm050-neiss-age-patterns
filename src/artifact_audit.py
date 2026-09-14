"""Content checks for execution and report audits; no external dependencies."""
import hashlib
import json
from pathlib import Path


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (FileNotFoundError, ValueError):
        return {}


def markdown_hash(notebook):
    """Counter scope, including references; the count display excludes itself."""
    texts = []
    for cell in notebook["cells"]:
        source = cell["source"]
        source = "".join(source) if isinstance(source, list) else source
        if cell["cell_type"] == "markdown" and not source.startswith("## Word Count"):
            texts.append(source)
    return hashlib.sha256(json.dumps(texts, ensure_ascii=False).encode()).hexdigest()


def checked_files(root, hashes):
    return bool(hashes) and all((root / name).is_file() and file_hash(root / name) == value
                                for name, value in hashes.items())


def counter_hash(notebook):
    sources = [(''.join(c['source']) if isinstance(c['source'], list) else c['source'])
               for c in notebook.get('cells', []) if c['cell_type'] == 'code']
    counters = [s for s in sources if s.startswith('%%js')]
    return hashlib.sha256(counters[0].encode()).hexdigest() if len(counters) == 1 else None


def report_checks(root):
    root = Path(root)
    audit = read_json(root / "report/word_counter_verification.json")
    final = read_json(root / "report/final_verification.json")
    report = root / "report/DSM050_Report_Revised.docx"
    pdf = root / "report/DSM050_Report_Revised.pdf"
    notebook = read_json(root / "notebooks/DSM050_Report_Word_Count.ipynb")
    same_report = report.is_file() and file_hash(report) == audit.get("source_report_sha256")
    same_markdown = bool(notebook) and markdown_hash(notebook) == audit.get("report_markdown_sha256")
    same_counter = counter_hash(notebook) == audit.get('counter_source_sha256')
    counter = same_report and same_markdown and same_counter
    pdf_current = (same_report and pdf.is_file() and
                   file_hash(pdf) == final.get("report_pdf_sha256") and
                   file_hash(report) == final.get("report_docx_sha256"))
    figures_current = checked_files(root, final.get("figure_hashes", {}))
    return {"official_counter_current": counter,
            "word_count": audit.get("official_main_count") if counter else None,
            "pdf_count_current": bool(counter and pdf_current),
            "figures_review_current": bool(figures_current and final.get("all_pdf_pages_visually_reviewed"))}

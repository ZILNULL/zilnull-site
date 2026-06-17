import shutil
import sys
from pathlib import Path

from src.files import read_file, write_file
from src.generation.renderer import render_page
from src.generation.writing_index import build_writing_index

_STATIC_DIR    = Path("website/static")
_TEMPLATES_DIR = Path("website/templates")
_CONTENT_DIR   = Path("website/content")
_DIST_DIR      = Path("dist")


def main() -> int:
    if _DIST_DIR.is_dir():
        shutil.rmtree(_DIST_DIR)
    _DIST_DIR.mkdir(parents=True)

    if _STATIC_DIR.is_dir():
        shutil.copytree(_STATIC_DIR, _DIST_DIR / "static")
        print(f"  copy  {_STATIC_DIR}/ -> {_DIST_DIR}/static/")

    for name in ("index.html", "contactme.html"):
        src = _TEMPLATES_DIR / name
        if src.exists():
            dst = _DIST_DIR / name
            shutil.copy2(src, dst)
            print(f"  copy  {src} -> {dst}")

    # Writing index (auto-generated from content/writing/ subdirs)
    writing_tmpl_path = _TEMPLATES_DIR / "writing.html"
    if not writing_tmpl_path.exists():
        print(f"Error: template not found at {writing_tmpl_path}", file=sys.stderr)
        return 1

    first_cat, shelf = build_writing_index(_CONTENT_DIR)
    writing_html = (
        read_file(writing_tmpl_path)
        .replace("{{ first_category }}", first_cat)
        .replace("{{ shelf_sections }}", shelf)
    )
    out_writing = _DIST_DIR / "writing" / "index.html"
    out_writing.parent.mkdir(parents=True, exist_ok=True)
    write_file(out_writing, writing_html)
    print(f"  build writing index -> {out_writing}")

    # Content pages from markdown
    text_tmpl_path = _TEMPLATES_DIR / "text.html"
    if not text_tmpl_path.exists():
        print(f"Error: template not found at {text_tmpl_path}", file=sys.stderr)
        return 1
    text_tmpl = read_file(text_tmpl_path)

    for md_file in sorted(_CONTENT_DIR.glob("writing/**/*.md")):
        rel = md_file.relative_to(_CONTENT_DIR).with_suffix(".html")
        out = _DIST_DIR / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        html = render_page(read_file(md_file), text_tmpl, "")
        write_file(out, html)
        print(f"  build {md_file} -> {out}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

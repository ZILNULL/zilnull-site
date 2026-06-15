import sys
from pathlib import Path

from src.files import copy_folder, read_file, write_file
from src.generation.toc import build_toc
from src.generation.renderer import render_page
from src.generation.styles import build_css

_CONTENT_DIR = Path("website/content")
_TEMPLATE_DIR = Path("website/templates")
_STATIC_DIR = Path("website/static")
_DIST_DIR = Path("dist")


def main() -> int:
    if _STATIC_DIR.is_dir():
        copy_folder(_STATIC_DIR, _DIST_DIR / "static")

    (_DIST_DIR / "static").mkdir(parents=True, exist_ok=True)
    write_file(_DIST_DIR / "static" / "index.css", build_css())

    template_path = _TEMPLATE_DIR / "template.html"
    if not template_path.exists():
        print(f"Error: template not found at {template_path}", file=sys.stderr)
        return 1
    template = read_file(template_path)

    _DIST_DIR.mkdir(parents=True, exist_ok=True)
    for md_file in _CONTENT_DIR.glob("**/*.md"):
        toc = build_toc(_CONTENT_DIR, md_file)
        html = render_page(read_file(md_file), template, toc)

        out_path = _DIST_DIR / md_file.relative_to(_CONTENT_DIR).with_suffix(".html")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        write_file(out_path, html)
        print(f"  {md_file} -> {out_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

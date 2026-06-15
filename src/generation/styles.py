from pathlib import Path

_STYLES_DIR = Path("website/styles")
_PARTIALS = [
    "vars.css",
    "reset.css",
    "layout.css",
    "sidebar.css",
    "toc.css",
    "typography.css",
    "code.css",
    "blockquote.css",
    "footnotes.css",
    "scrollbar.css",
    "responsive.css",
]


def build_css() -> str:
    return "\n".join((_STYLES_DIR / name).read_text() for name in _PARTIALS)

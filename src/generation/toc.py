from pathlib import Path


def _toc_dir(root: Path, path: Path, current_md: Path, lines: list[str]) -> None:
    entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    dirs = [e for e in entries if e.is_dir() and not e.name.startswith(".")]
    files = [e for e in entries if e.is_file() and e.suffix == ".md"]

    lines.append('<ul class="toc-list">')
    for d in dirs:
        lines.append('<li>')
        lines.append(f'<details class="toc-folder" open>')
        lines.append(f'<summary class="toc-dir-name">{d.name}</summary>')
        _toc_dir(root, d, current_md, lines)
        lines.append('</details>')
        lines.append('</li>')
    for f in files:
        href = "/" + f.relative_to(root).with_suffix(".html").as_posix()
        name = f.stem.replace("-", " ").replace("_", " ").title()
        active = ' class="active"' if f == current_md else ""
        lines.append(f'<li><a href="{href}"{active}>{name}</a></li>')
    lines.append("</ul>")


def build_toc(content_dir: Path, current_md: Path) -> str:
    lines: list[str] = []
    _toc_dir(content_dir, content_dir, current_md, lines)
    return "\n".join(lines)

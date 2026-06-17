from pathlib import Path

from src.conversion.frontmatter import parse_frontmatter
from src.files import read_file


def _label(name: str) -> str:
    return name.replace("-", " ").replace("_", " ").title()


def build_writing_index(content_dir: Path) -> tuple[str, str]:
    writing_dir = content_dir / "writing"
    if not writing_dir.is_dir():
        return ("", "")

    categories = sorted(
        (d for d in writing_dir.iterdir() if d.is_dir() and not d.name.startswith(".")),
        key=lambda d: d.name,
    )
    if not categories:
        return ("", "")

    first_category = _label(categories[0].name)
    sections: list[str] = []

    for cat_dir in categories:
        cat_label = _label(cat_dir.name)
        md_files = sorted(cat_dir.glob("**/*.md"), key=lambda p: p.stem)

        books: list[str] = []
        for md in md_files:
            meta, _ = parse_frontmatter(read_file(md))
            title = meta.get("title", _label(md.stem))
            bh    = meta.get("book_height", "80%")
            bw    = meta.get("book_width", "36px")
            href  = "/" + md.relative_to(content_dir).with_suffix(".html").as_posix()
            books.append(
                f'        <a class="book" href="{href}" style="--bh:{bh};--bw:{bw}">\n'
                f'          <span class="spine">{title}</span>\n'
                f'        </a>'
            )

        rows = ['      <div class="shelf-row">']
        rows.extend(books)
        rows.append("      </div>")
        rows.append('      <div class="shelf-row"></div>')
        rows.append('      <div class="shelf-row"></div>')

        sections.append(
            f'    <section class="shelf-section" data-category="{cat_label}">\n'
            + "\n".join(rows)
            + "\n    </section>"
        )

    return (first_category, "\n\n".join(sections))

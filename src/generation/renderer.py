from src.conversion.frontmatter import parse_frontmatter
from src.conversion.md_conversion import md_conversion


def render_page(md_text: str, template: str, toc: str) -> str:
    meta, body = parse_frontmatter(md_text)
    content_html = md_conversion(body).to_html()
    title = meta.get("title", "")
    return (
        template
        .replace("{{ title }}", title)
        .replace("{{ content }}", content_html)
        .replace("{{ toc }}", toc)
    )

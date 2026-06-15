import re

from src.models.htmlnode import _escape_html
from src.conversion.inline.spans import try_code_span, find_closing
from src.conversion.inline.links import try_link, make_link_html
from src.conversion.inline.footnotes import try_footnote_ref, get_footnotes

_ESCAPABLE = set("!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~")
_AUTOLINK = re.compile(r"<([a-zA-Z][a-zA-Z0-9+.\-]{1,31}://[^>\s<]*)>")
_EMAIL_AUTOLINK = re.compile(
    r"<([a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+"
    r"@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
    r"(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*)>"
)


def parse_inline(text: str) -> str:
    result: list[str] = []
    i = 0
    n = len(text)

    while i < n:
        c = text[i]

        if c == "\\" and i + 1 < n and text[i + 1] in _ESCAPABLE:
            result.append(_escape_html(text[i + 1]))
            i += 2
            continue

        if c == "`":
            if (m := try_code_span(text, i, n)) is not None:
                i, html = m
                result.append(html)
                continue

        if c == "!" and i + 1 < n and text[i + 1] == "[":
            if (lm := try_link(text, i + 1, n, is_image=True)) is not None:
                end, link_text, url, title, is_image = lm
                result.append(make_link_html(link_text, url, title, is_image, parse_inline))
                i = end
                continue

        if c == "[":
            if i + 1 < n and text[i + 1] == "^":
                if (m := try_footnote_ref(text, i, n)) is not None:
                    i, html = m
                    result.append(html)
                    continue
            if (lm := try_link(text, i, n, is_image=False)) is not None:
                end, link_text, url, title, is_image = lm
                result.append(make_link_html(link_text, url, title, is_image, parse_inline))
                i = end
                continue

        if c == "<":
            if match := _AUTOLINK.match(text, i):
                url = match.group(1)
                result.append(f'<a href="{_escape_html(url)}">{_escape_html(url)}</a>')
                i = match.end()
                continue
            if match := _EMAIL_AUTOLINK.match(text, i):
                email = match.group(1)
                result.append(
                    f'<a href="mailto:{_escape_html(email)}">{_escape_html(email)}</a>'
                )
                i = match.end()
                continue

        if c == "~" and text[i : i + 2] == "~~":
            if (m := find_closing(text, i, "~~", n)) is not None:
                i, inner = m
                result.append(f"<del>{parse_inline(inner)}</del>")
                continue

        if c in ("*", "_") and text[i : i + 3] == c * 3:
            if (m := find_closing(text, i, c * 3, n)) is not None:
                i, inner = m
                result.append(f"<em><strong>{parse_inline(inner)}</strong></em>")
                continue

        if c in ("*", "_") and text[i : i + 2] == c * 2:
            if (m := find_closing(text, i, c * 2, n)) is not None:
                i, inner = m
                result.append(f"<strong>{parse_inline(inner)}</strong>")
                continue

        if c in ("*", "_"):
            if c == "_":
                prev = text[i - 1] if i > 0 else " "
                if prev.isalnum() or prev == "_":
                    result.append(_escape_html(c))
                    i += 1
                    continue
            if (m := find_closing(text, i, c, n)) is not None:
                i, inner = m
                result.append(f"<em>{parse_inline(inner)}</em>")
                continue

        if c == "\n":
            trailing = 0
            j = len(result) - 1
            while j >= 0 and result[j] == " ":
                trailing += 1
                j -= 1
            if trailing >= 2:
                del result[len(result) - trailing :]
                result.append("<br />\n")
            else:
                result.append("\n")
            i += 1
            continue

        result.append(_escape_html(c))
        i += 1

    return "".join(result)


def render_footnote_section() -> str:
    footnotes = get_footnotes()
    if not footnotes:
        return ""
    parts = ['<section class="footnotes">\n<ol>']
    for fn_id, content in footnotes.items():
        content_html = parse_inline(content)
        backref = f'<a href="#fnref:{fn_id}" class="footnote-back">&#8617;</a>'
        parts.append(f'<li id="fn:{fn_id}">{content_html}\xa0{backref}</li>')
    parts.append("</ol>\n</section>")
    return "\n".join(parts)

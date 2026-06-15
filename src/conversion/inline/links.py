from collections.abc import Callable

from src.models.htmlnode import _escape_html

_refs: dict[str, tuple[str, str]] = {}


def set_refs(refs: dict[str, tuple[str, str]]) -> None:
    global _refs
    _refs = refs


def try_link(
    text: str, bracket_start: int, n: int, is_image: bool
) -> tuple[int, str, str, str, bool] | None:
    depth = 1
    i = bracket_start + 1
    while i < n and depth > 0:
        if text[i] == "[":
            depth += 1
        elif text[i] == "]":
            depth -= 1
        i += 1
    if depth != 0:
        return None

    bracket_end = i - 1
    link_text = text[bracket_start + 1 : bracket_end]

    if i < n and text[i] == "(":
        depth = 1
        i += 1
        paren_inner_start = i
        while i < n and depth > 0:
            if text[i] == "(":
                depth += 1
            elif text[i] == ")":
                depth -= 1
            i += 1
        if depth != 0:
            return None
        dest_and_title = text[paren_inner_start : i - 1].strip()
        url, title = _parse_dest_title(dest_and_title)
        return i, link_text, url, title, is_image

    if i < n and text[i] == "[":
        j = i + 1
        while j < n and text[j] != "]" and text[j] != "\n":
            j += 1
        if j < n and text[j] == "]":
            ref_text = text[i + 1 : j].strip()
            label = (ref_text or link_text).strip().lower()
            if label in _refs:
                url, title = _refs[label]
                return j + 1, link_text, url, title, is_image

    label = link_text.strip().lower()
    if label in _refs:
        url, title = _refs[label]
        return i, link_text, url, title, is_image

    return None


def make_link_html(
    link_text: str,
    url: str,
    title: str,
    is_image: bool,
    parse_inline: Callable[[str], str],
) -> str:
    title_attr = f' title="{_escape_html(title)}"' if title else ""
    if is_image:
        return f'<img src="{_escape_html(url)}" alt="{_escape_html(link_text)}"{title_attr} />'
    inner = parse_inline(link_text)
    return f'<a href="{_escape_html(url)}"{title_attr}>{inner}</a>'


def _parse_dest_title(s: str) -> tuple[str, str]:
    s = s.strip()
    if not s:
        return "", ""
    if s.startswith("<"):
        end = s.find(">")
        if end != -1:
            return s[1:end], _extract_title(s[end + 1 :])
    parts = s.split(None, 1)
    url = parts[0]
    title = _extract_title(parts[1]) if len(parts) > 1 else ""
    return url, title


def _extract_title(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and (
        (s[0] == '"' and s[-1] == '"')
        or (s[0] == "'" and s[-1] == "'")
        or (s[0] == "(" and s[-1] == ")")
    ):
        return s[1:-1]
    return ""

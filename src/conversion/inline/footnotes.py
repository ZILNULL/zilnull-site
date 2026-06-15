_footnotes: dict[str, str] = {}


def set_footnotes(footnotes: dict[str, str]) -> None:
    global _footnotes
    _footnotes = footnotes


def get_footnotes() -> dict[str, str]:
    return _footnotes


def _get_footnote_num(fn_id: str) -> int:
    for i, key in enumerate(_footnotes.keys(), 1):
        if key == fn_id:
            return i
    return 0


def try_footnote_ref(text: str, start: int, n: int) -> tuple[int, str] | None:
    j = start + 2
    while j < n and text[j] != "]" and text[j] != "\n":
        j += 1
    if j >= n or text[j] != "]":
        return None
    fn_id = text[start + 2 : j].strip()
    if not fn_id or fn_id not in _footnotes:
        return None
    num = _get_footnote_num(fn_id)
    html = f'<sup id="fnref:{fn_id}"><a href="#fn:{fn_id}">{num}</a></sup>'
    return j + 1, html

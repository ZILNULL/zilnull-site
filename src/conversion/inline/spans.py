from src.models.htmlnode import _escape_html


def try_code_span(text: str, start: int, n: int) -> tuple[int, str] | None:
    i = start
    while i < n and text[i] == "`":
        i += 1
    ticks = i - start

    k = i
    while k < n:
        if text[k] == "`":
            run_start = k
            while k < n and text[k] == "`":
                k += 1
            if k - run_start == ticks:
                content = text[i:run_start]
                content = content.replace("\n", " ")
                if len(content) > 2 and content[0] == " " and content[-1] == " ":
                    content = content[1:-1]
                return k, f"<code>{_escape_html(content)}</code>"
        else:
            k += 1

    return None


def find_closing(text: str, start: int, delim: str, n: int) -> tuple[int, str] | None:
    dlen = len(delim)
    i = start + dlen
    while i < n:
        if text[i] == delim[0]:
            run_start = i
            while i < n and text[i] == delim[0]:
                i += 1
            if i - run_start == dlen:
                return i, text[start + dlen : run_start]
        else:
            i += 1
    return None

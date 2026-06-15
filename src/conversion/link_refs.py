import re

_LINK_DEF = re.compile(
    r'^ {0,3}\[([^\[\]\n]+)\]:[ \t]*'
    r'(?:<([^<>\n]*)>|([^\s]+))'
    r'(?:[ \t]+(?:"([^"\n]*)"|\'([^\'\n]*)\'|\(([^)\n]*)\)))?'
    r'[ \t]*$',
    re.MULTILINE,
)

_FN_START = re.compile(r'^\[\^([^\[\]\n]+)\]:[ \t]*(.*)')


def extract_link_defs(text: str) -> tuple[dict[str, tuple[str, str]], str]:
    refs: dict[str, tuple[str, str]] = {}

    def _replace(m: re.Match) -> str:
        label = m.group(1).strip().lower()
        url = (m.group(2) if m.group(2) is not None else m.group(3) or "").strip()
        title = m.group(4) or m.group(5) or m.group(6) or ""
        refs.setdefault(label, (url, title))  # first definition wins
        return ""

    cleaned = _LINK_DEF.sub(_replace, text)
    return refs, cleaned


def extract_footnote_defs(text: str) -> tuple[dict[str, str], str]:
    footnotes: dict[str, str] = {}
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    i = 0
    while i < len(lines):
        m = _FN_START.match(lines[i])
        if m:
            fn_id = m.group(1).strip()
            content = m.group(2)
            i += 1
            while i < len(lines) and (
                lines[i].startswith("    ") or lines[i].startswith("\t")
            ):
                content += "\n" + re.sub(r"^(    |\t)", "", lines[i].rstrip("\n"))
                i += 1
            footnotes.setdefault(fn_id, content.strip())
        else:
            out.append(lines[i])
            i += 1
    return footnotes, "".join(out)

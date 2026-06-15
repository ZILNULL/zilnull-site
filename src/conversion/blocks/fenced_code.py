import re

from src.models.blocktypes import BlockType
from src.models.htmlnode import HTMLNode
from src.models.leafnode import LeafNode

_OPEN = re.compile(r"^[ ]{0,3}(`{3,}|~{3,})(.*)")


def valid_interruptions() -> list[BlockType]:
    return []


def new(fence_char: str, fence_len: int, info: str) -> HTMLNode:
    props: dict[str, str] = {"fence_char": fence_char, "fence_len": str(fence_len)}
    if info:
        props["info"] = info.split()[0]
    return LeafNode(BlockType.FENCED_CODE, "", props=props)


def still_matches(node: HTMLNode, new_line: str, interrupted: bool) -> bool:
    props = node.props or {}
    fence_char = props.get("fence_char", "`")
    fence_len = int(props.get("fence_len", "3"))

    rstripped = new_line.rstrip(" \t")
    inner = rstripped.lstrip(" ")
    leading = len(rstripped) - len(inner)
    if leading <= 3 and len(inner) >= fence_len and all(c == fence_char for c in inner):
        node.matched = False
        node.consumed = True
        return False

    node.value = (node.value or "") + new_line + "\n"
    node.matched = True
    return True


def close(node: HTMLNode):
    return


def matches(new_line: str) -> tuple[HTMLNode | None, bool]:
    m = _OPEN.match(new_line)
    if not m:
        return None, False

    fence = m.group(1)
    fence_char = fence[0]
    fence_len = len(fence)
    info = m.group(2).strip()

    if fence_char == "`" and "`" in info:
        return None, False

    return new(fence_char, fence_len, info), True

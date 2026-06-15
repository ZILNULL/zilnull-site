import re

from src.models.blocktypes import BlockType
from src.models.htmlnode import HTMLNode
from src.models.leafnode import LeafNode

_UNORDERED = re.compile(r"^([ ]{0,3})([-*+])([ \t]+)(.*)", re.DOTALL)
_ORDERED = re.compile(r"^([ ]{0,3})(\d{1,9})([.)]) +(.*)", re.DOTALL)


def valid_interruptions() -> list[BlockType]:
    return [
        BlockType.BLANK,
        BlockType.ATX_HEADING,
        BlockType.THEMATIC_BREAK,
        BlockType.FENCED_CODE,
        BlockType.BLOCK_QUOTE,
    ]


def new(content: str, list_type: str, content_col: int) -> HTMLNode:
    node = LeafNode(BlockType.LIST_ITEM, content)
    node.props = {"list_type": list_type, "content_col": str(content_col)}
    return node


def still_matches(node: HTMLNode, new_line: str, interrupted: bool) -> bool:
    if interrupted:
        node.matched = False
        return False

    content_col = int((node.props or {}).get("content_col", "2"))
    if len(new_line) >= content_col and new_line[:content_col].strip() == "":
        node.value = (node.value or "") + "\n" + new_line[content_col:]
        node.matched = True
        return True

    node.matched = False
    return False


def close(node: HTMLNode):
    if node.value is not None:
        node.value = node.value.strip()


def matches(new_line: str) -> tuple[HTMLNode | None, bool]:
    m = _UNORDERED.match(new_line)
    if m:
        indent = len(m.group(1))
        space_len = len(m.group(3))
        content_col = indent + 1 + space_len
        return new(m.group(4), "ul", content_col), True

    m = _ORDERED.match(new_line)
    if m:
        indent = len(m.group(1))
        marker_len = len(m.group(2)) + 1
        content_col = indent + marker_len + 1
        return new(m.group(4), "ol", content_col), True

    return None, False

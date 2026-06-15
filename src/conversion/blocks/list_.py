import re

from src.models.blocktypes import BlockType
from src.models.htmlnode import HTMLNode

_UNORDERED = re.compile(r"^[ ]{0,3}[-*+][ \t]+")
_ORDERED = re.compile(r"^[ ]{0,3}\d{1,9}[.)] +")


def valid_interruptions() -> list[BlockType]:
    return [
        BlockType.BLANK,
        BlockType.ATX_HEADING,
        BlockType.THEMATIC_BREAK,
        BlockType.FENCED_CODE,
        BlockType.BLOCK_QUOTE,
    ]


def still_matches(node: HTMLNode, new_line: str, interrupted: bool) -> bool:
    if interrupted:
        node.matched = False
        return False

    list_type = (node.props or {}).get("list_type", "ul")

    if list_type == "ul" and _UNORDERED.match(new_line):
        node.matched = True
        return True
    if list_type == "ol" and _ORDERED.match(new_line):
        node.matched = True
        return True

    if node.children:
        last_item = node.children[-1]
        content_col = int((last_item.props or {}).get("content_col", "2"))
        if len(new_line) >= content_col and new_line[:content_col].strip() == "":
            node.matched = True
            return True

    node.matched = False
    return False


def close(node: HTMLNode):
    return


def matches(new_line: str) -> tuple[HTMLNode | None, bool]:
    return None, False

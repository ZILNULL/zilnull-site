import re

from src.models.blocktypes import BlockType
from src.models.htmlnode import HTMLNode
from src.models.leafnode import LeafNode

_INDENT = re.compile(r"^(    |\t)(.*)", re.DOTALL)


def valid_interruptions() -> list[BlockType]:
    return []


def new(content: str) -> HTMLNode:
    return LeafNode(BlockType.INDENTED_CODE, content)


def still_matches(node: HTMLNode, new_line: str, interrupted: bool) -> bool:
    if interrupted:
        node.matched = False
        return False

    m = _INDENT.match(new_line)
    if m:
        node.value = (node.value or "") + m.group(2) + "\n"
        node.matched = True
        return True

    if not new_line.strip():
        node.value = (node.value or "") + "\n"
        node.matched = True
        return True

    node.matched = False
    return False


def close(node: HTMLNode):
    if node.value:
        node.value = node.value.rstrip("\n") + "\n"


def matches(new_line: str) -> tuple[HTMLNode | None, bool]:
    m = _INDENT.match(new_line)
    if m:
        return new(m.group(2) + "\n"), True
    return None, False

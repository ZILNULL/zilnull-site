import re
from collections.abc import Callable

from src.models.blocktypes import BlockType
from src.models.containernode import ContainerNode
from src.models.htmlnode import HTMLNode

_MARKER = re.compile(r"^[ ]{0,3}>[ ]?(.*)", re.DOTALL)
_block_parse_fn: Callable[[str], HTMLNode] | None = None


def set_block_parse(fn: Callable[[str], HTMLNode]) -> None:
    global _block_parse_fn
    _block_parse_fn = fn


def valid_interruptions() -> list[BlockType]:
    return [BlockType.BLANK]


def new(inner_line: str) -> HTMLNode:
    node = ContainerNode(BlockType.BLOCK_QUOTE, [], tag="blockquote")
    node.value = inner_line + "\n"
    return node


def still_matches(node: HTMLNode, new_line: str, interrupted: bool) -> bool:
    if interrupted:
        node.matched = False
        return False

    m = _MARKER.match(new_line)
    if m:
        node.value = (node.value or "") + m.group(1) + "\n"
        node.matched = True
        return True

    if new_line.strip():
        node.value = (node.value or "") + new_line + "\n"
        node.matched = True
        return True

    node.matched = False
    return False


def close(node: HTMLNode) -> None:
    if node.value is None or _block_parse_fn is None:
        return
    inner_doc = _block_parse_fn(node.value)
    node.children = inner_doc.children
    node.value = None


def matches(new_line: str) -> tuple[HTMLNode | None, bool]:
    m = _MARKER.match(new_line)
    if m:
        return new(m.group(1)), True
    return None, False

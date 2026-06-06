from src.models.blocktypes import BlockType
from src.models.htmlnode import HTMLNode
from src.models.leafnode import LeafNode


def valid_interruptions() -> list[BlockType]:
    return [BlockType.BLANK, BlockType.ATX_HEADING]


def new(text: str) -> HTMLNode:
    return LeafNode(BlockType.PARAGRAPH, text)


def still_matches(node: HTMLNode, new_line: str, interrupted: bool) -> bool:
    node.matched = interrupted
    return interrupted


def close(node: HTMLNode):
    if node.value is None:
        return

    node.value = node.value.strip()


def matches(new_line: str) -> tuple[HTMLNode | None, bool]:
    return new(new_line), True

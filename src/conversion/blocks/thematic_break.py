import re

from src.models.blocktypes import BlockType
from src.models.htmlnode import HTMLNode
from src.models.leafnode import LeafNode

_PATTERN = re.compile(
    r"^[ ]{0,3}((?:\*[ \t]*){3,}|(?:-[ \t]*){3,}|(?:_[ \t]*){3,})[ \t]*$"
)


def valid_interruptions() -> list[BlockType]:
    return []


def new() -> HTMLNode:
    return LeafNode(BlockType.THEMATIC_BREAK, "", tag="hr")


def still_matches(node: HTMLNode, new_line: str, interrupted: bool) -> bool:
    node.matched = False
    return False


def close(node: HTMLNode):
    return


def matches(new_line: str) -> tuple[HTMLNode | None, bool]:
    if _PATTERN.match(new_line):
        return new(), True
    return None, False

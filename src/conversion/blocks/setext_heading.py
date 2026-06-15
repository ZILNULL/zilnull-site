from src.models.blocktypes import BlockType
from src.models.htmlnode import HTMLNode


def valid_interruptions() -> list[BlockType]:
    return []


def still_matches(node: HTMLNode, new_line: str, interrupted: bool) -> bool:
    node.matched = False
    return False


def close(node: HTMLNode):
    if node.value is not None:
        node.value = node.value.strip()


def matches(new_line: str) -> tuple[HTMLNode | None, bool]:
    return None, False

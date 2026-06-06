from src.models.blocktypes import BlockType
from src.models.htmlnode import HTMLNode


def valid_interruptions() -> list[BlockType]:
    return []


def new(text: str) -> HTMLNode:
    return HTMLNode()


def still_matches(node: HTMLNode, new_line: str, interrupted: bool) -> bool:
    return False


def close(node: HTMLNode):
    return None


def matches(new_line: str) -> tuple[HTMLNode | None, bool]:
    return None, new_line.isspace()

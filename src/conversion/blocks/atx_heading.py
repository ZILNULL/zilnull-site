from src.models.blocktypes import BlockType
from src.models.htmlnode import HTMLNode
from src.models.leafnode import LeafNode


def valid_interruptions() -> list[BlockType]:
    return []


def new(text: str, h_count: int = 1) -> HTMLNode:
    return LeafNode(BlockType.ATX_HEADING, text, tag=f"h{h_count}")


def still_matches(node: HTMLNode, new_line: str, interrupted: bool) -> bool:
    node.matched = False
    return False


def close(node: HTMLNode):
    return


def matches(new_line: str) -> tuple[HTMLNode | None, bool]:
    stripped = new_line.lstrip(" ")
    if len(new_line) - len(stripped) > 3:
        return None, False

    if not stripped or stripped[0] != "#":
        return None, False

    h_count = 0
    for c in stripped:
        if c != "#":
            break
        h_count += 1

    if h_count > 6:
        return None, False

    rest = stripped[h_count:]
    if rest and rest[0] not in (" ", "\t"):
        return None, False

    content = rest.lstrip(" \t").rstrip(" \t")

    if content.endswith("#"):
        i = len(content) - 1
        while i >= 0 and content[i] == "#":
            i -= 1
        if i < 0 or content[i] in (" ", "\t"):
            content = content[: i + 1].rstrip(" \t") if i >= 0 else ""

    return new(content, h_count), True

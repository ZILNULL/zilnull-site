from src.models.blocktypes import BlockType
from src.models.htmlnode import HTMLNode
from src.models.leafnode import LeafNode


def valid_interruptions() -> list[BlockType]:
    return []


def new(text: str, h_count: int = 1) -> HTMLNode:
    tag = f"h{h_count}"
    return LeafNode(BlockType.ATX_HEADING, text, tag=tag)


def still_matches(node: HTMLNode, new_line: str, interrupted: bool) -> bool:
    node.matched = False
    return False


def close(node: HTMLNode):
    return


def matches(new_line: str) -> tuple[HTMLNode | None, bool]:
    start_spaces = new_line.count(" ", 0, 4)
    if start_spaces > 3:
        return None, False

    new_line = new_line.lstrip()
    if new_line[0] != "#":
        return None, False

    h_count = 0
    for c in new_line:
        if c != "#":
            break
        h_count += 1

    if h_count > 6:
        return None, False

    if not new_line[h_count].isspace():
        return None, False

    # Strip trailing # and spaces:
    new_line = new_line.strip()
    last_index = len(new_line)
    while new_line[last_index] == "#":
        last_index -= 1

        if last_index == 0 or (
            new_line[last_index] != "#" and not new_line[last_index].isspace()
        ):
            break

        if new_line[last_index].isspace():
            new_line = new_line[:last_index]
            break

    return new(new_line, h_count), True

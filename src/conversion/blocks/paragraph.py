from src.models.blocktypes import BlockType
from src.models.htmlnode import HTMLNode
from src.models.leafnode import LeafNode


def valid_interruptions() -> list[BlockType]:
    return [
        BlockType.BLANK,
        BlockType.ATX_HEADING,
        BlockType.THEMATIC_BREAK,
        BlockType.FENCED_CODE,
        BlockType.BLOCK_QUOTE,
        BlockType.LIST_ITEM,
    ]


def new(text: str) -> HTMLNode:
    return LeafNode(BlockType.PARAGRAPH, text, tag="p")


def _is_setext_underline(line: str, char: str) -> bool:
    stripped = line.rstrip(" \t")
    content = stripped.lstrip(" ")
    if len(stripped) - len(content) > 3:
        return False
    return len(content) >= 1 and all(c == char for c in content)


def still_matches(node: HTMLNode, new_line: str, interrupted: bool) -> bool:
    if _is_setext_underline(new_line, "="):
        node.blocktype = BlockType.SETEXT_HEADING
        node.tag = "h1"
        node.matched = False
        return False
    if _is_setext_underline(new_line, "-"):
        node.blocktype = BlockType.SETEXT_HEADING
        node.tag = "h2"
        node.matched = False
        return False

    if interrupted:
        node.matched = False
        return False

    node.value = (node.value or "") + "\n" + new_line
    node.matched = True
    return True


def close(node: HTMLNode):
    if node.value is not None:
        node.value = node.value.strip()


def matches(new_line: str) -> tuple[HTMLNode | None, bool]:
    if not new_line.strip():
        return None, False
    return new(new_line), True

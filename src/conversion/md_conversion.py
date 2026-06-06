from src.conversion.blocks.blockparser import BlockParser
from src.models.blocktypes import BlockType
from src.models.containernode import ContainerNode
from src.models.htmlnode import HTMLNode
from .blocks import atx_heading, paragraph, blank

_blocks: dict[BlockType, BlockParser] = {
    BlockType.ATX_HEADING: atx_heading,
    BlockType.PARAGRAPH: paragraph,
    BlockType.BLANK: blank,
}
_order = [BlockType.BLANK, BlockType.ATX_HEADING, BlockType.PARAGRAPH]


def md_conversion(md: str) -> HTMLNode:
    document = ContainerNode(BlockType.DOCUMENT, [])
    lines = md.splitlines()
    for line in lines:
        new_block = None

        # Check matches:
        curr_node = document
        while curr_node.children and len(curr_node.children) > 0:
            open_node = curr_node.children[-1]
            if open_node.blocktype is None:
                break

            parser = _blocks[open_node.blocktype]
            allowed = parser.valid_interruptions()
            interrupted = False
            for a in allowed:
                if new_block and a == new_block.blocktype:
                    interrupted = True
                    break

                block, match = _blocks[a].matches(line)
                if match and block is not None:
                    new_block = block
                    interrupted = True
                    break

            _ = _blocks[open_node.blocktype].still_matches(open_node, line, interrupted)
            curr_node = open_node

        # New block start?
        for blocktype in _order:
            if new_block is not None:
                break

            parser = _blocks[blocktype]
            block, match = parser.matches(line)
            if match and block is not None:
                new_block = block
                break

        if new_block is not None:
            last_matched = document
            curr_node = document
            while curr_node.children and len(curr_node.children) > 0:
                open_node = curr_node.children[-1]
                if not open_node.matched:
                    if open_node.blocktype is None:
                        break

                    _blocks[open_node.blocktype].close(curr_node)
                    curr_node = open_node
                    continue

                curr_node = open_node
                last_matched = curr_node

            if last_matched.children is None:
                last_matched.children = []
            last_matched.children.append(new_block)

    return document

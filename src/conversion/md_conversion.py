from src.conversion.blocks.blockparser import BlockParser
from src.conversion.link_refs import extract_link_defs, extract_footnote_defs
from src.conversion.inline.links import set_refs
from src.conversion.inline.footnotes import set_footnotes
from src.conversion.inline.parser import render_footnote_section
from src.models.blocktypes import BlockType
from src.models.containernode import ContainerNode
from src.models.htmlnode import HTMLNode
from src.models.leafnode import LeafNode
from .blocks import (
    atx_heading,
    paragraph,
    blank,
    setext_heading,
    thematic_break,
    indented_code,
    fenced_code,
    block_quote,
    list_,
    list_item,
)

_blocks: dict[BlockType, BlockParser] = {
    BlockType.ATX_HEADING: atx_heading,
    BlockType.PARAGRAPH: paragraph,
    BlockType.BLANK: blank,
    BlockType.SETEXT_HEADING: setext_heading,
    BlockType.THEMATIC_BREAK: thematic_break,
    BlockType.INDENTED_CODE: indented_code,
    BlockType.FENCED_CODE: fenced_code,
    BlockType.BLOCK_QUOTE: block_quote,
    BlockType.LIST: list_,
    BlockType.LIST_ITEM: list_item,
}

_order = [
    BlockType.BLANK,
    BlockType.THEMATIC_BREAK,
    BlockType.ATX_HEADING,
    BlockType.FENCED_CODE,
    BlockType.INDENTED_CODE,
    BlockType.BLOCK_QUOTE,
    BlockType.LIST_ITEM,
    BlockType.PARAGRAPH,
]


def md_conversion(md: str) -> HTMLNode:
    refs, body = extract_link_defs(md)
    footnotes, body = extract_footnote_defs(body)
    set_refs(refs)
    set_footnotes(footnotes)

    document = _block_parse(body)

    fn_html = render_footnote_section()
    if fn_html:
        document.children.append(LeafNode(BlockType.RAW, fn_html))

    return document


def _block_parse(md: str) -> HTMLNode:
    document = ContainerNode(BlockType.DOCUMENT, [])
    lines = md.splitlines()
    for line in lines:
        new_block = None

        line_consumed = False
        curr_node = document
        while curr_node.children:
            open_node = curr_node.children[-1]
            if open_node.blocktype is None or open_node.blocktype not in _blocks:
                break

            if not open_node.matched:
                break

            parser = _blocks[open_node.blocktype]
            allowed = parser.valid_interruptions()
            interrupted = False
            for a in allowed:
                if new_block and a == new_block.blocktype:
                    interrupted = True
                    break

                block, match = _blocks[a].matches(line)
                if match:
                    if block is not None:
                        new_block = block
                    interrupted = True
                    break

            old_blocktype = open_node.blocktype
            still_open = _blocks[old_blocktype].still_matches(
                open_node, line, interrupted
            )

            line_consumed = still_open
            if open_node.consumed:
                line_consumed = True
                open_node.consumed = False

            if (
                old_blocktype == BlockType.PARAGRAPH
                and open_node.blocktype == BlockType.SETEXT_HEADING
            ):
                new_block = None
                line_consumed = True

            curr_node = open_node

        if not line_consumed:
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
            while curr_node.children:
                open_node = curr_node.children[-1]
                if not open_node.matched:
                    if open_node.blocktype is not None and open_node.blocktype in _blocks:
                        _blocks[open_node.blocktype].close(open_node)
                    break

                curr_node = open_node
                last_matched = curr_node

            if new_block.blocktype == BlockType.LIST_ITEM:
                ltype = (new_block.props or {}).get("list_type", "ul")
                if (
                    last_matched.blocktype == BlockType.LIST
                    and (last_matched.props or {}).get("list_type") == ltype
                ):
                    last_matched.children.append(new_block)
                    new_block = None
                else:
                    tag = "ul" if ltype == "ul" else "ol"
                    wrapper = ContainerNode(BlockType.LIST, [new_block], tag=tag)
                    wrapper.props = {"list_type": ltype}
                    new_block = wrapper

            if new_block is not None:
                last_matched.children.append(new_block)

    _finalize(document)
    return document


def _finalize(node: HTMLNode) -> None:
    for child in node.children:
        _finalize(child)
    if node.blocktype and node.blocktype in _blocks:
        _blocks[node.blocktype].close(node)


block_quote.set_block_parse(_block_parse)

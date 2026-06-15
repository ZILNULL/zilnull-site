from enum import Enum


class BlockType(Enum):
    DOCUMENT = "document"
    BLANK = "blank"
    PARAGRAPH = "paragraph"
    ATX_HEADING = "atx_heading"
    SETEXT_HEADING = "setext_heading"
    THEMATIC_BREAK = "thematic_break"
    INDENTED_CODE = "indented_code"
    FENCED_CODE = "fenced_code"
    BLOCK_QUOTE = "block_quote"
    LIST = "list"
    LIST_ITEM = "list_item"
    RAW = "raw"

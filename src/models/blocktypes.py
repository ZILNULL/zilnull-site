from enum import Enum


class BlockType(Enum):
    DOCUMENT = "document"
    BLANK = "blank"
    PARAGRAPH = "paragraph"
    ATX_HEADING = "atx_heading"

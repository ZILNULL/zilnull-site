from src.models.blocktypes import BlockType
from src.models.htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        blocktype: BlockType | None,
        value: str,
        tag: str | None = None,
        props: dict[str, str] | None = None,
    ):
        super().__init__(blocktype=blocktype, tag=tag, value=value, props=props)

    def __repr__(self):
        stringified = f"LeafNode(blocktype={self.blocktype}, tag={self.tag}, value={self.value}, props=[{self.props_to_html()}])"
        return stringified

    def to_html(self) -> str:
        return ""

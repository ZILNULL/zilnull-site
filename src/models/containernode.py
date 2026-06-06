from src.models.blocktypes import BlockType
from src.models.htmlnode import HTMLNode


class ContainerNode(HTMLNode):
    def __init__(
        self,
        blocktype: BlockType,
        children: list["HTMLNode"],
        tag: str | None = None,
        props: dict[str, str] | None = None,
    ):
        super().__init__(blocktype=blocktype, tag=tag, children=children, props=props)

    def __repr__(self):
        stringified = f"ContainerNode(blocktype={self.blocktype}, tag={self.tag}, children={str(self.children)}, props=[{self.props_to_html()}])"
        return stringified

    def to_html(self) -> str:
        return ""

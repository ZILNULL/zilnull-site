from src.models.blocktypes import BlockType
from src.models.htmlnode import HTMLNode, _escape_html
from src.conversion.inline.parser import parse_inline


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
        if self.blocktype == BlockType.RAW:
            return self.value or ""
        if self.blocktype == BlockType.BLANK:
            return ""
        if self.blocktype == BlockType.THEMATIC_BREAK:
            return "<hr />"

        if self.blocktype in (BlockType.INDENTED_CODE, BlockType.FENCED_CODE):
            info = (self.props or {}).get("info", "")
            lang_attr = f' class="language-{_escape_html(info)}"' if info else ""
            return f"<pre><code{lang_attr}>{_escape_html(self.value or '')}</code></pre>"

        value = parse_inline(self.value or "")

        if self.blocktype == BlockType.LIST_ITEM:
            return f"<li>{value}</li>"

        if self.tag:
            return f"<{self.tag}>{value}</{self.tag}>"

        return value

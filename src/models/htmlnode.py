from src.models.blocktypes import BlockType


def _escape_html(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


class HTMLNode:
    def __init__(
        self,
        blocktype: BlockType | None = None,
        tag: str | None = None,
        value: str | None = None,
        children: list["HTMLNode"] | None = None,
        props: dict[str, str] | None = None,
        matched: bool = True,
    ):
        self.blocktype = blocktype
        self.tag = tag
        self.value = value
        self.children: list["HTMLNode"] = children if children is not None else []
        self.props = props
        self.matched = matched
        self.consumed = False

    def __eq__(self, other: object):
        if not isinstance(other, HTMLNode):
            return False

        equal = (
            self.blocktype == other.blocktype
            and self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )
        return equal

    def __repr__(self):
        stringified = f"HTMLNode(blocktype={self.blocktype}, tag={self.tag}, value={self.value}, children={str(self.children)}, props=[{self.props_to_html()}])"
        return stringified

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props is None or len(self.props) == 0:
            return ""

        stringified = ""
        for key in self.props:
            stringified += f'{key}="{self.props[key]}" '
        return stringified[: len(stringified) - 1]

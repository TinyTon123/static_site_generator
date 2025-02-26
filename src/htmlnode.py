
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ""
        for k, v in self.props.items():
            result += f' {k}="{v}"'
        return result

    def __repr__(self):
        tag = self.tag
        value = self.value
        children = self.children
        props = self.props_to_html()
        return f"{self.__class__.__name__}({tag}, {value}, {children}, {props})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        if not self.props:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, children=children, value=None, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError(f"{self.__class__.__name__} must have a tag")
        if not self.children:
            raise ValueError(f"{self.__class__.__name__} must have at least one child node")
        else:
            result = ""
            if self.children:
                for child in self.children:
                    result += child.to_html()
            
            return f"<{self.tag}>{result}</{self.tag}>"


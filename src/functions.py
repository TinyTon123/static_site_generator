import re

from htmlnode import LeafNode
from textnode import TextType, TextNode


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a",
                value=text_node.text,
                props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img",
                value="",
                props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError

def split_nodes_delimiter(old_nodes: list, delimiter, text_type) -> list:
        result = []
        for old_node in old_nodes:
            if old_node.text_type != TextType.TEXT:
                result.append(old_node)
            else:
                if old_node.text.count(delimiter) % 2 != 0:
                    raise SyntaxError(
                        f"Invalid Markdown syntax. Closing {delimiter} was never closed"
                        )
                else:
                    text_split = old_node.text.split(delimiter)
                    for indx, piece in enumerate(text_split):
                        if piece == "":
                            continue
                        if indx % 2 == 0:
                            result.append(
                                TextNode(piece, TextType.TEXT)
                                )
                        else:
                            result.append(
                                TextNode(piece, text_type)
                                )
        
        return result


def extract_markdown_images(text):
    regex = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex, text)

def extract_markdown_links(text):
    regex = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(regex, text)

def split_nodes_image(old_nodes: list):
    result = []
    regex_to_split_by = r"(!\[[^\[\]]*\]\([^\(\)]*\))"
    
    for old_node in old_nodes:
        split_text: list = re.split(regex_to_split_by, old_node.text)
        if len(split_text) == 1:
            result.append(old_node)
        else:
            for piece in split_text:
                if piece == "":
                    continue
                images = extract_markdown_images(piece)
                if images:
                    result.append(
                        TextNode(images[0][0], TextType.IMAGE, images[0][1])
                        )
                else:
                    result.append(
                        TextNode(piece, TextType.TEXT)
                    )

    return result

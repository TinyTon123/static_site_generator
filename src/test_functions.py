import unittest

from functions import (
    text_node_to_html_node, split_nodes_delimiter,
    extract_markdown_images, extract_markdown_links,
    split_nodes_image
)
from htmlnode import LeafNode
from textnode import TextType, TextNode

class TestFunctions(unittest.TestCase):
    # def test_textnode_to_htmlnode(self):
    #     converted_node = (
    #         text_node_to_html_node(TextNode("just text", TextType.TEXT))
    #     )
    #     converted_node2 = (
    #         text_node_to_html_node(
    #             TextNode("url url", TextType.LINK, "www.y.com")
    #             )
    #     )
    #     converted_node3 = (
    #         text_node_to_html_node(TextNode("bold text", TextType.BOLD))
    #     )
    #     converted_node4 = (
    #         text_node_to_html_node(
    #             TextNode("alt text", TextType.IMAGE, "www.img.com")
    #             )
    #     )

    #     self.assertEqual(
    #         converted_node.to_html(),
    #         "just text"
    #     )

    def test_split_nodes_delimiter(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        node1 = TextNode("bold text", TextType.BOLD)
        node2 = TextNode("Not *italic text*", TextType.TEXT)
        node3 = TextNode("**NEW bold text**???", TextType.TEXT)
        node4 = TextNode(
            "How do you like this **bold** *italic* and `code` text?",
            TextType.TEXT
            )

        new_nodes = split_nodes_delimiter(
            [node, node1, node2, node3, node4],
            "`", TextType.CODE
            )

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT, None),
                TextNode("code block", TextType.CODE, None),
                TextNode(" word", TextType.TEXT, None),
                TextNode("bold text", TextType.BOLD, None),
                TextNode("Not *italic text*", TextType.TEXT, None),
                TextNode("**NEW bold text**???", TextType.TEXT, None),
                TextNode(
                    "How do you like this **bold** *italic* and ",
                    TextType.TEXT, None
                    ),
                TextNode("code", TextType.CODE, None),
                TextNode(" text?", TextType.TEXT, None)
            ]
            )

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([
            ("image", "https://i.imgur.com/zjjcJKZ.png")
        ], matches)

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) "
        text += "and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "Abracadabra",
            TextType.TEXT,
        )
        node3 = TextNode(
            "No, this text has no image, but a link [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        node4 = TextNode(
            "![Imagine Dragons](https://blablabla.com/Dragon.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node, node2, node3, node4])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("Abracadabra", TextType.TEXT),
                TextNode(
                    "No, this text has no image, but a link [link](https://i.imgur.com/zjjcJKZ.png)",
                    TextType.TEXT,
                ),
                TextNode("Imagine Dragons", TextType.IMAGE, "https://blablabla.com/Dragon.jpeg"),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()

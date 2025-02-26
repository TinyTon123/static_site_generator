import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextType, TextNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(props={
            "a1": "b1",
            "a2": "b2",
            "a3": "b3"
        })
        node2 = HTMLNode(props={
            "test_prop": "test_value"
        })
        node3 = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
        })

        self.assertEqual(
            node.props_to_html(),
            ' a1="b1" a2="b2" a3="b3"'
        )
        self.assertEqual(
            node3.props_to_html(),
            ' href="https://www.google.com" target="_blank"')
        self.assertEqual(
            node2.props_to_html(),
            ' test_prop="test_value"'
        )

    def test_to_html(self):
        leaf = LeafNode("p", "test text")
        leaf2 = LeafNode("a", "krya krya", props={"href": "https://www.google.com"})
        leaf3 = LeafNode("b", "bla bla bla", props={"hires": "www@com"})

        self.assertEqual(
            leaf.to_html(),
            '<p>test text</p>'
        )
        self.assertEqual(
            leaf2.to_html(),
            '<a href="https://www.google.com">krya krya</a>'
        )
        self.assertEqual(
            leaf3.to_html(),
            '<b hires="www@com">bla bla bla</b>'
        )

    def test_parent_node(self):
        parent_node = ParentNode(
        "G",
        [ParentNode("p",[
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        ),
        ParentNode("p",[
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        )
        ]
        )
        self.assertEqual(
            parent_node.to_html(),
            "<G><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></G>"
        )


if __name__ == "__main__":
    unittest.main()

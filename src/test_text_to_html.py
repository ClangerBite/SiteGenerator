import unittest
from htmlnode import LeafNode
from textnode import TextNode, TextType
from text_to_html import text_node_to_html_node


class TestTextToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertIsInstance(html_node, LeafNode)
        
    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertIsInstance(html_node, LeafNode) 
        
    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertIsInstance(html_node, LeafNode)
        
    def test_code(self):
        node = TextNode("print('Hello, world!')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello, world!')")
        self.assertIsInstance(html_node, LeafNode) 
        
    def test_link(self):
        node = TextNode("Google", TextType.LINK, url="https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})
        self.assertIsInstance(html_node, LeafNode)
        
    def test_image(self):
        node = TextNode("An image", TextType.IMAGE, url="https://www.example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertIsNone(html_node.value)
        self.assertEqual(html_node.props, {"src": "https://www.example.com/image.png", "alt": "An image"})
        self.assertIsInstance(html_node, LeafNode)

    def test_wrong_type(self):
        with self.assertRaises(ValueError) as ctx:    
            node = TextNode("This is a text node", "HELLO")
            text_node_to_html_node(node)
            self.assertIn("Unknown TextType", str(ctx.exception))
    

    


if __name__ == "__main__":
    unittest.main()
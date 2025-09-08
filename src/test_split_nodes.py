import unittest

from textnode import TextNode, TextType
from split_nodes import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks


class TestSplitNodes(unittest.TestCase):

    def test_code_block_in_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        split = split_nodes_delimiter([node], "`", TextType.CODE)
        answer = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(split, answer)
        
    def test_two_code_blocks_in_text(self):
        node = TextNode("This is text with a `code block` word with `more code block`", TextType.TEXT)
        split = split_nodes_delimiter([node], "`", TextType.CODE)
        answer = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word with ", TextType.TEXT),
            TextNode("more code block", TextType.CODE),
        ]
        self.assertEqual(split, answer)
        
    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        split = split_nodes_delimiter([node], "**", TextType.BOLD)
        further_split = split_nodes_delimiter(split, "_", TextType.ITALIC)
        answer = [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ]
        self.assertEqual(further_split, answer)
        
    def test_unmatched_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)   
        self.assertTrue("unmatched delimiter" in str(context.exception))

        
class TestExtractLinks(unittest.TestCase):
    
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        answer = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        returned = extract_markdown_images(text)
        self.assertListEqual(returned, answer)
        
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        answer = [
            ("to boot dev", "https://www.boot.dev"), 
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        returned = extract_markdown_links(text)
        self.assertListEqual(returned, answer)
        

class TestSplitImages(unittest.TestCase):
    
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        answer = [("image", "https://i.imgur.com/zjjcJKZ.png")]
        returned = extract_markdown_images(text)
        self.assertListEqual(returned, answer)
        
    def test_split_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
        answer =  [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ]        
        node = TextNode(text, TextType.TEXT)
        returned = split_nodes_image([node])
        self.assertListEqual(returned, answer)

    def test_split_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        answer = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]       
        node = TextNode(text, TextType.TEXT)
        returned = split_nodes_link([node])
        self.assertListEqual(returned, answer)      



class TestTextToTextNodes(unittest.TestCase):
        
    def test_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        answer =  [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]      
        returned = text_to_textnodes(text)
        self.assertListEqual(returned, answer)



class TestMarkdownToBlocks(unittest.TestCase):

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        returned = markdown_to_blocks(md)
        answer = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        
        self.assertListEqual(returned, answer)
        
        
    def test_markdown_to_blocks_with_multiple_newlines(self):
        md = """
This is **bolded** paragraph





This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""
        returned = markdown_to_blocks(md)
        answer = [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        
        self.assertListEqual(returned, answer)

if __name__ == "__main__":
    unittest.main()
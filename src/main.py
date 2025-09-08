from textnode import TextNode, TextType
from split_nodes import text_to_textnodes, markdown_to_blocks

def main():

    
    # text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    # returned = text_to_textnodes(text)
    
    # answer =  [
    #         TextNode("This is ", TextType.TEXT),
    #         TextNode("text", TextType.BOLD),
    #         TextNode(" with an ", TextType.TEXT),
    #         TextNode("italic", TextType.ITALIC),
    #         TextNode(" word and a ", TextType.TEXT),
    #         TextNode("code block", TextType.CODE),
    #         TextNode(" and an ", TextType.TEXT),
    #         TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
    #         TextNode(" and a ", TextType.TEXT),
    #         TextNode("link", TextType.LINK, "https://boot.dev"),
    #     ]
    
    # print(answer == returned)

  
    md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
    returned = markdown_to_blocks(md)
    answer =[
            "This is **bolded** paragraph",
            "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items",
        ]
    print(answer == returned)




if __name__ == "__main__":
    main()

from textnode import TextType, TextNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)

      #check if delimiter is in the text
        elif delimiter in node.text:
            parts = node.text.split(delimiter)
            if len(parts)%2 == 0:
                raise ValueError(f"Invalid Markdown syntax due to unmatched delimiter: {delimiter} in text: {node.text}")      
            
            for i, part in enumerate(parts):
                if i%2 == 0:
                    type = TextType.TEXT
                else:
                    type = text_type
                if part != "":
                    new_node = TextNode(text=part, text_type=type)
                    new_nodes.append(new_node)

        else:
            new_nodes.append(node)
    return new_nodes  

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    images = [(alt_text, url) for alt_text, url in matches]
    return images

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    links = [(link_text, url) for link_text, url in matches]
    return links

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        images = extract_markdown_images(node.text)
        number_of_images = len(images)
        if number_of_images == 0:
            new_nodes.append(node) 
            continue
        
        text = node.text
        
        for image in images:
            parts = []
            parts = text.split(f"![{image[0]}]({image[1]})", 1)
            
            if parts[0] == "":
                new_image_node = TextNode(text=image[0], text_type=TextType.IMAGE, url=image[1])
                new_nodes.append(new_image_node)
            else:
                new_text_node = TextNode(text=parts[0], text_type=TextType.TEXT)
                new_nodes.append(new_text_node)
                new_image_node = TextNode(text=image[0], text_type=TextType.IMAGE, url=image[1])
                new_nodes.append(new_image_node) 
            
            text = parts[1]
        
        if text !="":
            new_text_node = TextNode(text=text, text_type=TextType.TEXT)
            new_nodes.append(new_text_node)
                    
    return new_nodes


def split_nodes_link(old_nodes):    
   
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        links = extract_markdown_links(node.text)
        number_of_links = len(links)

        if number_of_links == 0:
            new_nodes.append(node) 
            continue
        
        text = node.text
        
        for link in links:
            parts = []
            parts = text.split(f"[{link[0]}]({link[1]})", 1)
            
            if parts[0] == "":
                new_link_node = TextNode(text=link[0], text_type=TextType.LINK, url=link[1])
                new_nodes.append(new_link_node)
            else:
                new_text_node = TextNode(text=parts[0], text_type=TextType.TEXT)
                new_nodes.append(new_text_node)
                new_link_node = TextNode(text=link[0], text_type=TextType.LINK, url=link[1])
                new_nodes.append(new_link_node) 
            text = parts[1]
            
        if text !="":
            new_text_node = TextNode(text=text, text_type=TextType.TEXT)
            new_nodes.append(new_text_node)
                    
    return new_nodes

def text_to_textnodes(text):
    nodes = TextNode(text, TextType.TEXT)
    nodes = [nodes]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    
    return nodes

# def show_nodes(nodes):
#     for node in nodes:
#         print(node, "\n")
#     print("****************************************")


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block != "":
            filtered_blocks.append(block.strip())
    
    return filtered_blocks
    

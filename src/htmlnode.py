class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value      
        self.children = children
        self.props = props
        

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props is None:
            return None
        return " " + " ".join(f'{item}="{self.props[item]}"' for item in self.props)
        
    def __repr__(self):    
        return f"Tag: {self.tag}\n, Value: {self.value}\n, Props: {self.props}\n, Children: {self.children}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        
        props_str = self.props_to_html() or ""
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
        

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
            
        children_html = "".join(child.to_html() for child in self.children)        
        props_str = self.props_to_html() or ""
        
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"
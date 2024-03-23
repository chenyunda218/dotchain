from .node import Node

class Statement(Node):
    
    def __init__(self) -> None:
        self.type = "Statement"
    
    def dict(self):
        return {
            "type": self.type
        }
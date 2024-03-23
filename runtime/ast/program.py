from .statement import Statement
from .node import Node

class Program(Node):
    
    def __init__(self, body: list[Statement]) -> None:
        self.body = body

    def dict(self):
        return {
            "type": "Program",
            "body": [b.dict() for b in self.body]
        }
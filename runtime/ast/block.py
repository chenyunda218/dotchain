from .statement import Statement

class Block(Statement):
    
    def __init__(self, body: list[Statement]) -> None:
        self.body = body
    
    def dict(self):
        return {
            "type": "Block",
            "body": [b.dict() for b in self.body],
        }
from .statement import Statement

class Identifier(Statement):
    
    def __init__(self, name):
        self.name = name

    def dict(self):
        return {
            "type": "Identifier",
            "name": self.name
        }
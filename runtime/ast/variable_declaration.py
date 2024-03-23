from .fun import Fun
from .literal.literal import Literal
from .identifier import Identifier
from .statement import Statement

class VariableDeclaration(Statement):
    
    def __init__(self, identifier: Identifier, value: Literal | Fun) -> None:
        self.id = identifier
        self.value = value
    
    def dict(self):
        return {
            "type": "VariableDeclaration",
            "id": self.id.dict(),
            "value": self.value.dict(),
        }
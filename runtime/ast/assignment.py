from .identifier import Identifier
from .statement import Statement


class Assignment(Statement):
    
    def __init__(self, id: Identifier, value) -> None:
        self.id = id
        self.value = value

    def dict(self):
        return {
            "type": "Assignment",
            "id": self.id.dict(),
            "value": self.value.dict()
        }
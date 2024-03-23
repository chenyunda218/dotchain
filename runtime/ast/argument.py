from .identifier import Identifier
from .statement import Statement


class Argument(Statement):

    def __init__(self, id: Identifier):
        self.id = id

    def dict(self):
        return {
            "type": "Argument",
            "id": self.id.dict(),
        }
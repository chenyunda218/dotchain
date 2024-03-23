
from .block import Block
from .argument import Argument
from .statement import Statement


class Fun(Statement):
    
    def __init__(self, params: list[any], body: Block) -> None:
        self.params = params
        self.body = body

    def dict(self):
        return {
            "type": "Fun",
            "params": [arg.dict() for arg in self.params],
            "body": self.body.dict(),
        }
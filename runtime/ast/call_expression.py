from .literal.literal import Literal
from .expression import Expression
from .identifier import Identifier


class CallExpression(Expression):
    
    def __init__(self, callee: Identifier, arguments: list[any]) -> None:
        self.callee = callee
        self.arguments = arguments

    def dict(self):
        return {
            "type": "CallExpression",
            "callee": self.callee.dict(),
            "arguments": [arg.dict() for arg in self.arguments]
        }
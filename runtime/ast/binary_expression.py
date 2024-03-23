from .statement import Statement


class BinaryExpression(Statement):
    
    def __init__(self, left: Statement, operator: str, right: Statement):
        self.left = left
        self.operator = operator
        self.right = right

    def dict(self):
        return {
            "type": "BinaryExpression",
            "left": self.left.dict(),
            "operator": self.operator,
            "right": self.right.dict(),
        }
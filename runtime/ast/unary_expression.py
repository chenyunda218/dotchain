from .expression import Expression


class UnaryExpression(Expression):
    def __init__(self, operator: str, expression: Expression):
        self.operator = operator
        self.expression = expression

    def dict(self):
        return {
            "type": "UnaryExpression",
            "operator": self.operator,
            "expression": self.expression.dict(),
        }
from runtime.ast.statement import Statement


class Literal(Statement):
      
    def __init__(self, value) -> None:
        self.value = value

    def dict(self):
        return {
            "type": "Literal",
            "value": self.value
        }
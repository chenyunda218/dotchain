from .literal import Literal

class NumericalLiteral(Literal):
        
    def __init__(self, value: int | float) -> None:
        self.value = value

    def dict(self):
        return {
            "type": "NumericalLiteral",
            "value": self.value
        }
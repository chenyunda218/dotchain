from .literal import Literal


class BoolLiteral(Literal):
    
    def __init__(self, value: bool):
        self.value = bool(value)

    def dict(self):
        return {
            "type": "BoolLiteral",
            "value": self.value
        }
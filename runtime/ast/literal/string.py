from .literal import Literal


class StringLiteral(Literal):
    
    def __init__(self, value: str):
        self.value = value[1:-1]

    def dict(self):
        return {
            "type": "StringLiteral",
            "value": self.value
        }
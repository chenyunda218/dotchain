from .numerical import NumericalLiteral


class IntLiteral(NumericalLiteral):
          
    def __init__(self, value: int) -> None:
        self.value = int(value)
    
    def dict(self):
        return {
            "type": "IntLiteral",
            "value": self.value
        }
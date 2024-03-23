from .numerical import NumericalLiteral


class FloatLiteral(NumericalLiteral):
        
    def __init__(self, value: float) -> None:
        self.value = float(value)
    
    def dict(self):
        return {
            "type": "FloatLiteral",
            "value": self.value
        }
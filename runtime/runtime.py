
from abc import ABC

class Context:
    
    def __init__(self, values=None) -> None:
        self.values = values if values is not None else {}
    
    def get_value(self, name: str):
        return self.values[name]
    
    def has_value(self, name: str):
        return name in self.values
    
    def show_values(self):
        for name in self.values:
            print(name, self.values[name])
    
    def set_value(self, name: str, value):
        self.values[name] = value

class Runtime(ABC):
    
    def __init__(self, context=None, parent=ABC) -> None:
        self.parent = parent
        self.context = context if context is not None else Context()
    
    def chain_has_value(self, name: str):
        if self.context.has_value(name):
            return True
        if self.parent is not None:
            return self.parent.chain_has_value(name)
        return False
    
    def has_value(self, name):
        return self.context.has_value(name)
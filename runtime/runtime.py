
from abc import ABC, abstractmethod

class Context:
    
    def __init__(self, values=None) -> None:
        self.values = values if values is not None else {}
    
    def get_value(self, name: str):
        return self.values.get(name)

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
    
    def has_value(self, name):
        return self.context.has_value(name)
    
    def show_values(self):
        self.context.show_values()

    def set_value(self, name: str, value):
        self.context.set_value(name, value)
    
    def get_value(self, name: str):
        return self.context.get_value(name)
    
    @abstractmethod
    def assign_value(self, name: str, value):
        pass

    @abstractmethod
    def declare_value(self, name: str, value):
        pass
    

from abc import ABC
from .ast import  Program, VariableDeclaration


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
    
    def __init__(self, context=None, parent=None) -> None:
        self.parent = parent
        self.context = context if context is not None else Context()

    def run(self, program: Program):
        self.program = program
        self.pointer = 0
        while self.pointer < len(self.program.body):
            statement = self.program.body[self.pointer]
            self.execute(statement)
            self.pointer += 1

    def execute(self, statement):
        if isinstance(statement, VariableDeclaration):
            self.variable_declaration(statement)
    
    def variable_declaration(self, statement: VariableDeclaration):
        self.context.set_value(statement.id.name, statement.value)
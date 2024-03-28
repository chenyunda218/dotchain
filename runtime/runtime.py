from ast import Expression
from runtime.ast import Block, CallExpression, Fun, Identifier, Literal, Program, ReturnStatement, Statement, VariableDeclaration

class Runtime():
    
    def __init__(self, context=None, parent=None, exteral_fun=None) -> None:
        self.parent = parent
        self.context = context if context is not None else dict()
        self.exteral_fun = exteral_fun if exteral_fun is not None else dict()

    def set_fun_body(self, body: Block):
        self.body = body

    def has_value(self, identifier: Identifier) -> bool:
        return identifier.name in self.context
    
    def get_value(self, identifier: Identifier):
        return self.context.get(identifier.name)
    
    def set_value(self, identifier: Identifier, value):
        self.context[identifier.name] = value
    
    def declare(self, identifier: Identifier, value):
        if self.has_value(identifier):
            raise Exception(f"Variable {identifier.name} is already declared")
        self.set_value(identifier, value)
    
    def assign(self, identifier: Identifier, value):
        if self.has_value(identifier):
            self.set_value(identifier, value)
        elif self.parent is not None:
            self.parent.assign(identifier, value)
        else:
            raise Exception(f"Variable {identifier} is not declared")
        
    def show_values(self):
        print(self.context)


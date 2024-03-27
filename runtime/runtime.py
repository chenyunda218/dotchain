from ast import Expression
from runtime.ast import CallExpression, Program, Statement, VariableDeclaration

class Runtime():
    
    def __init__(self, context=None, parent=None, exteral_fun=None) -> None:
        self.parent = parent
        self.context = context if context is not None else dict()
        self.exteral_fun = exteral_fun if exteral_fun is not None else dict()
    
    def has_value(self, identifier: str) -> bool:
        return identifier in self.context
    
    def get_value(self, identifier: str):
        return self.context.get(identifier)
    
    def set_value(self, identifier: str, value):
        self.context[identifier] = value
    
    def declare(self, identifier: str, value):
        if self.has_value(identifier):
            raise Exception(f"Variable {identifier} is already declared")
        self.context[identifier] = value
    
    def assign(self, identifier: str, value):
        if self.has_value(identifier):
            self.set_value(identifier, value)
        elif self.parent is not None:
            self.parent.assign(identifier, value)
        else:
            raise Exception(f"Variable {identifier} is not declared")
        
    def show_values(self):
        print(self.context)

def exec_statement(runtime: Runtime, statement: Statement):
    if isinstance(statement, Program):
        exec_program(runtime, statement)
    elif isinstance(statement, Program):
        exec_program(runtime, statement)
    elif isinstance(statement, CallExpression):
        exec_call_expression(runtime, statement)

def exec_call_expression(runtime: Runtime, call_expression: CallExpression):
    exec_exteral_function_call(runtime, call_expression)

def exec_exteral_function_call(runtime: Runtime, call_expression: CallExpression):
    pass

def exec_program(runtime: Runtime, program: Program):
    for statement in program.body:
        exec_statement(runtime, statement)

def exec_declaration(runtime: Runtime, declaration: VariableDeclaration):
    runtime.declare(declaration.id.name, exec_eval(runtime,declaration.value))

def exec_eval(runtime: Runtime, expression: Expression):
    if isinstance(expression, CallExpression):
        return exec_call_expression(runtime, expression)
    return None
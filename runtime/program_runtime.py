

from ast import Expression
from runtime.ast import Assignment, Identifier, IntLiteral, Literal, Program, Statement, StringLiteral, VariableDeclaration
from runtime.runtime import Context, Runtime

class ProgrameRuntime(Runtime):

    def exec(self, program: Program):
        for statement in program.body:
            exec_statement(self, statement)

    def show_values(self):
        self.context.show_values()
    
    def declare_value(self, name: str, value):
        if self.has_value(name):
            raise Exception(f"Variable {name} already declared")
        self.context.set_value(name, value)

    def assign_value(self, name: str, value):
        if not self.has_value(name):
            if self.parent is None or not self.parent.has_value(name):
                raise Exception(f"Variable {name} not defined")
            self.parent.assign_value(name, value)
        self.context.set_value(name, value)

    def has_value(self, name):
        return self.context.has_value(name)

    def set_value(self, name: str, value):
        self.context.set_value(name, value)
    
    def get_value(self, name: str):
        v = self.context.get_value(name)
        if v is None:
            if self.parent is None:
                raise Exception(f"Variable {name} not defined")
            return self.parent.get_value(name)
        return v
    
class BlockRuntime(Runtime):

    def __init__(self, context=None, parent=Runtime) -> None:
        super().__init__(context, parent)
    
    def exec(self, block):
        pass



def exec_statement(runtime: Runtime, statement: Statement):
    if isinstance(statement, VariableDeclaration):
        exec_variable_declaration(runtime, statement)
    elif isinstance(statement, Assignment):
        exec_assignment(runtime, statement)
    elif isinstance(statement, Expression):
        evaluate_expression(runtime, statement)

def exec_assignment(runtime: Runtime, assignment: Assignment):
    runtime.assign_value(assignment.id.name, 
                         evaluate_expression(runtime, assignment.value))

def exec_variable_declaration(runtime: Runtime, declaration: VariableDeclaration):
    runtime.declare_value(declaration.id.name, 
                          evaluate_expression(runtime, declaration.value))

def evaluate_expression(runtime: Runtime, expression: Expression):
    if isinstance(expression, Identifier):
        return runtime.get_value(expression.name)
    elif isinstance(expression, Literal):
        return expression.value
    else:
        raise Exception(f"Expression {expression} not supported")
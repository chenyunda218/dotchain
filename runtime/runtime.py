from ast import Expression
from runtime.ast import Block, CallExpression, Fun, Identifier, Literal, Program, Statement, VariableDeclaration


class Runtime():
    
    def __init__(self, context=None, parent=None, exteral_fun=None) -> None:
        self.parent = parent
        self.context = context if context is not None else dict()
        self.exteral_fun = exteral_fun if exteral_fun is not None else dict()

    def set_fun_body(self, body: Block):
        self.body = body

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
    elif isinstance(statement, Block):
        exec_block(runtime, statement)
    elif isinstance(statement, CallExpression):
        exec_call_expression(runtime, statement)
    elif isinstance(statement, VariableDeclaration):
        exec_declaration(runtime, statement)

def exec_block(runtime: Runtime, block: Block):
    for statement in block.body:
        exec_statement(runtime, statement)

def exec_fun_declaration(runtime: Runtime, function_declaration: VariableDeclaration):
    fun = Runtime(parent=runtime)
    fun.set_fun_body(function_declaration.value.body)
    runtime.declare(function_declaration.id.name, fun)

def exec_call_expression(runtime: Runtime, call_expression: CallExpression):
    if not runtime.has_value(call_expression.callee.name):
        if runtime.parent is not None:
            return exec_call_expression(runtime.parent, call_expression)
        return exec_exteral_function_call(runtime, call_expression)
    return exec_interal_function_call(runtime, call_expression)

def exec_interal_function_call(runtime: Runtime, call_expression: CallExpression):
    fun = runtime.get_value(call_expression.callee.name)
    return exec_block(fun, fun.body)
    

def exec_exteral_function_call(runtime: Runtime, call_expression: CallExpression):
    fun = runtime.exteral_fun.get(call_expression.callee.name)
    if fun is None:
        raise Exception(f"Function {call_expression.callee.name} is not defined")
    args = []
    for arg in call_expression.arguments:
        args.append(exec_eval(runtime, arg))
    fun(*args)

def exec_program(runtime: Runtime, program: Program):
    for statement in program.body:
        exec_statement(runtime, statement)

def exec_declaration(runtime: Runtime, declaration: VariableDeclaration):
    if isinstance(declaration.value, Fun):
        return exec_fun_declaration(runtime, declaration)
    runtime.declare(declaration.id.name, exec_eval(runtime,declaration.value))

def exec_eval(runtime: Runtime, expression: Expression):
    if isinstance(expression, Identifier):
        return runtime.get_value(expression.name)
    if isinstance(expression, Literal):
        return expression.value
    if isinstance(expression, CallExpression):
        return exec_call_expression(runtime, expression)
    return None
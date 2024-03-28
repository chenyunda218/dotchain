from ast import Expression
from runtime.ast import Assignment, BinaryExpression, Block, BoolLiteral, BreakStatement, CallExpression, EmptyStatement, FloatLiteral, Fun, Identifier, IfStatement, IntLiteral, Literal, Program, ReturnStatement, Statement, StringLiteral, UnaryExpression, VariableDeclaration, WhileStatement

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

def eval_literal(_: Runtime, literal: Literal):
    return literal.value

def eval_identifier(runtime: Runtime, identifier: Identifier):
    if runtime.has_value(identifier):
        return runtime.get_value(identifier)
    if runtime.parent is not None:
        return eval_identifier(runtime.parent, identifier)
    return None

def eval_binary_expression(runtime: Runtime, expression: BinaryExpression):
    left = eval(runtime, expression.left)
    right = eval(runtime, expression.right)
    if expression.operator == "+":
        return left + right
    if expression.operator == "-":
        return left - right
    if expression.operator == "*":
        return left * right
    if expression.operator == "/":
        return left / right
    if expression.operator == "%":
        return left % right
    if expression.operator == "<":
        return left < right
    if expression.operator == ">":
        return left > right
    if expression.operator == "<=":
        return left <= right
    if expression.operator == ">=":
        return left >= right
    if expression.operator == "==":
        return left == right
    if expression.operator == "!=":
        return left != right
    if expression.operator == "&&":
        return left and right
    if expression.operator == "||":
        return left or right
    raise Exception(f"Unknown operator {expression.operator}")

def eval_unary_expression(runtime: Runtime, unary_expression: UnaryExpression):
    value = eval(runtime, unary_expression.expression)
    if unary_expression.operator == "-":
        return -value
    if unary_expression.operator == "!":
        return not value
    return value

def eval_empty_statement(runtime: Runtime, _: EmptyStatement):
    return None

eval_map = {
    Literal: eval_literal,
    BoolLiteral: eval_literal,
    StringLiteral: eval_literal,
    IntLiteral: eval_literal,
    FloatLiteral: eval_literal,
    Identifier: eval_identifier,
    BinaryExpression: eval_binary_expression,
    UnaryExpression: eval_unary_expression,
    EmptyStatement: eval_empty_statement,
}

def eval(runtime: Runtime, expression: Expression):
    return eval_map[type(expression)](runtime, expression)

def exec_variable_declaration(runtime: Runtime, statement: VariableDeclaration):
    if runtime.has_value(statement.id):
        raise Exception(f"Variable {statement.id.name} is already declared")
    runtime.set_value(statement.id, eval(runtime, statement.value))

def exec_assignment(runtime: Runtime, statement: VariableDeclaration):
    if runtime.has_value(statement.id):
        runtime.set_value(statement.id, eval(runtime, statement.value))
    elif runtime.parent is not None:
        exec_assignment(runtime.parent, statement)
    else:
        raise Exception(f"Variable {statement.id} is not declared")

def exec_fun_call(runtime: Runtime, statement: CallExpression, exec_runtime: Runtime=None):
    if exec_runtime is None:
        exec_runtime = runtime
    if runtime.has_value(statement.callee):
        print("call interal")
    elif runtime.parent is not None:
        exec_fun_call(runtime, statement, exec_runtime)
    elif statement.callee.name in runtime.exteral_fun:
        args = [eval(exec_runtime, arg) for arg in statement.arguments]
        fun = runtime.exteral_fun[statement.callee.name]
        return fun(*args)
    else:
        raise Exception(f"Function {statement.callee.name} is not declared")

def exec_if_statement(runtime: Runtime, statement: IfStatement):
    new_runtime = Runtime(parent=runtime)
    if eval(runtime, statement.test):
        return exec_block(new_runtime, statement.consequent)
    elif statement.alternate is not None:
        return exec_block(new_runtime, statement.alternate)

def exec_while_statement(runtime: Runtime, statement: WhileStatement):
    new_runtime = Runtime(parent=runtime)
    while eval(new_runtime, statement.test):
        result = exec_block(new_runtime, statement.body)
        if result is not None:
            return result

def exec_block(runtime: Runtime, block: Block):
    for statement in block.body:
        if isinstance(statement, ReturnStatement):
            return eval(runtime, statement.value)
        if isinstance(statement, BreakStatement):
            break
        exec_statement(runtime, statement)

def exec_program(runtime: Runtime, program: Program):
    for statement in program.body:
        if isinstance(statement, ReturnStatement):
            return eval(runtime, statement.value)
        exec_statement(runtime, statement)

exec_map = {
    VariableDeclaration: exec_variable_declaration,
    Assignment: exec_assignment,
    IfStatement: exec_if_statement,
    WhileStatement: exec_while_statement,
    CallExpression: exec_fun_call,
}

def exec_statement(runtime: Runtime, statement: Statement):
    exec_map[type(statement)](runtime, statement)
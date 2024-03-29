from attr import dataclass
from runtime.ast import Assignment, BinaryExpression, Block, BoolLiteral, BreakStatement, CallExpression, EmptyStatement, FloatLiteral, Fun, Identifier, IfStatement, IntLiteral, Literal, Program, ReturnStatement, Statement, StringLiteral, UnaryExpression, VariableDeclaration, WhileStatement
from runtime.runtime import Runtime

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

def exec_fun_call(runtime: Runtime, statement: CallExpression, exec_runtime: Runtime=None):
    if exec_runtime is None:
        exec_runtime = runtime
    if runtime.has_value(statement.callee):
        result = exec_internal_fun_call(runtime, statement, exec_runtime)
        print(result)
        return result
    elif runtime.parent is not None:
        return exec_fun_call(runtime.parent, statement, exec_runtime)
    elif statement.callee.name in runtime.exteral_fun:
        args = [eval(exec_runtime, arg) for arg in statement.arguments]
        fun = runtime.exteral_fun[statement.callee.name]
        return fun(*args)
    else:
        raise Exception(f"Function {statement.callee.name} is not declared")

def exec_return_statement(runtime: Runtime, statement: ReturnStatement):
    return ReturnValue(eval(runtime))


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
    ReturnStatement: exec_return_statement,
}

def eval(runtime: Runtime, expression: Expression):
    return eval_map[type(expression)](runtime, expression)

def exec_variable_declaration(runtime: Runtime, statement: VariableDeclaration):
    if runtime.has_value(statement.id):
        raise Exception(f"Variable {statement.id.name} is already declared")
    if isinstance(statement.value, Fun):
        runtime.set_value(statement.id, FunEnv(runtime, statement.value))
    elif isinstance(statement.value, CallExpression):
        result = exec_fun_call(runtime, statement.value)
        if isinstance(result, ReturnValue):
            runtime.set_value(statement.id, result.value)
    else:
        runtime.set_value(statement.id, eval(runtime, statement.value))

def exec_assignment(runtime: Runtime, statement: Assignment):
    if runtime.has_value(statement.id):
        runtime.set_value(statement.id, eval(runtime, statement.value))
    elif runtime.parent is not None:
        exec_assignment(runtime.parent, statement)
    else:
        raise Exception(f"Variable {statement.id} is not declared")

def exec_internal_fun_call(runtime: Runtime, call: CallExpression, exec_runtime: Runtime):
    fun: FunEnv = runtime.get_value(call.callee)
    new_runtime = Runtime(parent=fun.parent)
    for index in range(len(fun.body.params)):
        new_runtime.set_value(fun.body.params[index], eval(exec_runtime, call.arguments[index]))
    new_runtime.show_values()
    result = exec_block(new_runtime, fun.body.body)
    print("###",result)
    return result

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
        if isinstance(result, BreakStatement):
            break
        if isinstance(result, ReturnValue):
            return ReturnValue
        if result is not None:
            return result

def exec_block(runtime: Runtime, block: Block):
    for statement in block.body:
        if isinstance(statement, ReturnStatement):
            print("@", statement)
            return ReturnValue(eval(runtime, statement.value))
        if isinstance(statement, BreakStatement):
            return statement
        result = exec_statement(runtime, statement)
        if isinstance(result, ReturnValue):
            print("@:",result)
            return result
        

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
    ReturnStatement: exec_return_statement,
}

def exec_statement(runtime: Runtime, statement: Statement):
    if isinstance(statement, WhileStatement):
        result = exec_while_statement(runtime, statement)
        print("@@",result)
        return result
    return exec_map[type(statement)](runtime, statement)
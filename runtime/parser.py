
from runtime.ast import Assignment, BinaryExpression, CallExpression, IntLiteral, Literal, Program, Statement, StringLiteral, UnaryExpression, VariableDeclaration
from .tokenizer import Tokenizer, Token


identifier = "IDENTIFIER"

class Parser():
    
    def __init__(self) -> None:
        self.tkr = Tokenizer()
        self.current_token = None
    
    def parse(self, script: str):
        t = Tokenizer()
        t.init(script)
        t.get_next_token()
        return program_parser(t)

def program_parser(tkr: Tokenizer):
    return Program(statement_list_parser(tkr))

def statement_list_parser(tkr: Tokenizer) -> list[Statement]:
    statement_list = []
    statement = statement_parser(tkr)
    while statement is not None:
        statement_list.append(statement)
        statement = statement_parser(tkr)
    return statement_list

def statement_parser(tkr: Tokenizer) -> Statement:
    token = tkr.get_current_token()
    if token is None:
        return None
    if token.type == "let":
        return let_parser(tkr)
    if _is_assignment(tkr):
        return assignment_parser(tkr)
    
def assignment_parser(tkr: Tokenizer):
    id = identifier_parser(tkr)
    tkr.eat("=")
    return Assignment(id, unquote_parser(tkr))

def let_parser(tkr: Tokenizer):
    tkr.eat("let")
    id = identifier_parser(tkr)
    tkr.eat("=")
    token = tkr.get_current_token()
    if _is_literal(token):
        unquoted = parse_literal(tkr)
    elif _is_func_dec(tkr):
        unquoted = fun_parser(tkr)
    else:
        unquoted = unquote_parser(tkr)
    if unquoted is None:
        raise Exception("Invalid variable declaration")
    return VariableDeclaration(id, unquoted)

def unquote_parser(tkr: Tokenizer):
    token = tkr.get_current_token()
    if _is_unary_expression(token):
        unquoted = unary_parser(tkr)
    elif _is_literal(token):
        unquoted = parse_literal(tkr)
    elif _is_func_call(tkr):
        unquoted = func_call_parser(tkr)
    elif _is_identifier(token):
        unquoted = identifier_parser(tkr)
    if _is_binary(tkr.clone().get_current_token()):
        print()
    return unquoted

def binary_parser(tkr: Tokenizer, unquoted):
    left = unquote_parser(tkr)
    operator = tkr.get_current_token().value
    tkr.eat(operator)
    right = unquote_parser(tkr)
    return BinaryExpression(left, operator, right)

def unary_parser(tkr: Tokenizer):
    token = tkr.get_current_token()
    tkr.eat(token.type)
    return UnaryExpression(token.value, unquote_parser(tkr))

def func_call_parser(tkr: Tokenizer):
    id = identifier_parser(tkr)
    tkr.eat("(")
    args = []
    while tkr.get_current_token().type != ")":
        args.append(unquote_parser(tkr))
        if tkr.get_current_token().type == ",":
            tkr.eat(",")
    return CallExpression(id, args)

def parse_literal(tkr: Tokenizer) -> Literal:
    token = tkr.get_current_token()
    if token.type == "STRING":
        return parse_string_literal(tkr)
    elif token.type == "INT":
        return parse_int_literal(tkr)
    elif token.type == "BOOL":
        return parse_bool_literal(tkr)
    elif token.type == "FLOAT":
        return parse_float_literal(tkr)
    raise Exception("Invalid literal")

def parse_string_literal(tkr: Tokenizer):
    token = tkr.eat("STRING")
    return StringLiteral(token.value)

def parse_int_literal(tkr: Tokenizer):
    token = tkr.eat("INT")
    return IntLiteral(token.value)

def parse_bool_literal(tkr: Tokenizer):
    token = tkr.eat("BOOL")
    return BoolLiteral(token.value)

def parse_float_literal(tkr: Tokenizer):
    token = tkr.eat("FLOAT")
    return FloatLiteral(token.value)

def identifier_parser(tkr: Tokenizer):
    token = tkr.eat(identifier)
    return Identifier(token.value)

def fun_parser(tkr: Tokenizer):
    tkr.eat("(")
    args = list[Identifier]()
    while tkr.get_current_token().type != ")":
        id = identifier_parser(tkr)
        args.append(id)
        if tkr.get_current_token().type == ",":
            tkr.eat(",")
    tkr.eat(")")
    tkr.eat("=>")
    return Fun(args, block_parser(tkr))

def block_parser(tkr: Tokenizer):
    tkr.eat("{")
    statements = statement_list_parser(tkr)
    tkr.eat("}")
    return Block(statements)
    
def _is_func_call(tkr: Tokenizer):
    tkr = tkr.clone()
    token = tkr.get_current_token()
    if _is_identifier(token):
        tkr.eat(identifier)
        if tkr.get_current_token().type == "(":
            return True
    return False

def _is_func_dec(tkr: Tokenizer):
    tkr = tkr.clone()
    token = tkr.get_current_token()
    if token.type != "(":
        return False
    tkr.eat("(")
    while True:
        tokenType = tkr.get_current_token().type
        if tokenType == ")":
            tkr.eat(")")
            break
        if tokenType == identifier:
            tkr.eat(identifier)
        if tokenType == ",":
            tkr.eat(",")
    if tkr.get_current_token().type == "=>":
        return True
    return False

def _is_literal(token: Token):
    return token.type in ["STRING", "INT", "BOOL", "FLOAT"]

def _is_identifier(token: Token):
    return token.type == identifier

def _is_assignment(tkr: Tokenizer):
    tkr = tkr.clone()
    if _is_identifier(tkr.get_current_token()):
        tkr.eat(identifier)
        if tkr.get_current_token().type == "=":
            return True
    return False

def _is_binary(token: Token):
    return token.value in ["+", "-", "*", "/", "%", "<", ">", "<=", ">=", "!=", "==", "&&", "||"]

def _is_logical_operator(token: Token):
    return token.type in ["&&", "||"]

def _is_comparison_operator(token: Token):
    return token.type in ["<", ">", "<=", ">=", "!=", "=="]

def _is_arithmetic_operator(token: Token):
    return token.type in ["+", "-", "*", "/", "%"]

def _is_unary_expression(token: Token):
    return token.value in ["!", "+", "-"]

def _priority(token: Token):
    if token.value in ["(", ")"]:
        return 1
    if _is_unary_expression(token):
        return 2
    if token.value in ["*", "/", "%"]:
        return 3
    if token.value in ["+", "-"]:
        return 4
    if token.value in ["<", ">", "<=", ">=", "!=", "=="]:
        return 5
    if token.value in ["&&"]:
        return 6
    if token.value in ["||"]:
        return 7
    return 999
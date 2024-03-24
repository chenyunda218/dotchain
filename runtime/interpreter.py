from ast import Expression
from runtime.ast import Assignment, BoolLiteral, EmptyStatement, FloatLiteral, Identifier, IntLiteral, Program, Statement, StringLiteral, UnaryExpression, VariableDeclaration
from .tokenizer import Token, Tokenizer

identifier_string = "IDENTIFIER"

class Interpreter:
    
    def __init__(self) -> None:
        self.tkr = Tokenizer()

    def _get_token(self) -> Token:
        return self.tkr.current_token
    
    def _get_token_type(self) -> str:
        if self.tkr.current_token is None:
            return None
        return self.tkr.current_token.type

    def parse(self, script: str):
        self.tkr.init(script)
        self.tkr.get_next_token()
        return self.program()
    
    def program(self):
        body = list[Statement]()
        while self._get_token() is not None:
            body.append(self.statement())
        return Program(body)
    
    def statement(self):
        token = self._get_token()
        if token.value == "let":
            return self.let()
        return self.assignment()
    
    def assignment(self):
        id = self.identifier()
        self.tkr.eat("=")
        expression = self.expression()
        return Assignment(id, expression)

    def let(self):
        self.tkr.eat("let")
        id = self.identifier()
        self.tkr.eat("=")
        expression = self.expression()
        return VariableDeclaration(id, expression)
    
    def expression(self, stack: list[Expression] = []):
        tokenType = self._get_token_type()
        if tokenType is None:
            raise Exception("Unexpected EOF")
        if tokenType == "INT":
            return self.int_literal()
        elif tokenType == "FLOAT":
            return self.float_literal()
        elif tokenType == "STRING":
            return self.string_literal()
        elif tokenType == "BOOL":
            return self.bool_literal()
        if tokenType == ";":
            self.tkr.eat(";")
            return EmptyStatement()
        if _is_unary(self._get_token()):
            token = self.tkr.eat(self._get_token_type())
            expression = UnaryExpression(token.value, self.expression())
        if self._get_token_type() == ";":
            return expression
    
    def int_literal(self):
        return int_literal(self.tkr)
    
    def float_literal(self):
        return float_literal(self.tkr)
    
    def string_literal(self):
        return string_literal(self.tkr)
    
    def bool_literal(self):
        return bool_literal(self.tkr)

    def identifier(self):
        return identifier(self.tkr)

def int_literal(tkr: Tokenizer):
        token = tkr.eat("INT")
        return IntLiteral(int(token.value))
    
def float_literal(tkr: Tokenizer):
    token = tkr.eat("FLOAT")
    return FloatLiteral(float(token.value))

def string_literal(tkr: Tokenizer):
    token = tkr.eat("STRING")
    return StringLiteral(token.value[1:-1])

def bool_literal(tkr: Tokenizer):
    token = tkr.eat("BOOL")
    if token.value == "true":
        return BoolLiteral(True)
    return BoolLiteral(False)

def identifier(tkr: Tokenizer):
    token = tkr.get_current_token()
    tkr.eat(identifier_string)
    return Identifier(token.value)

def binary_expression(stack: list[Token] = None):
    if stack is None or len(stack) == 0:
        return []
    operator_stack = list[Token]()
    output_stack = list[Token]()
    for token in stack:
        if token.value == "(":
            operator_stack.append(token)
        elif _is_operator(token):
            if len(operator_stack) == 0 or _priority(token) > _priority(operator_stack[-1]):
                operator_stack.append(token)
        else:
            output_stack.append(token)
    return output_stack

def _is_operator(token: Token):
    return token.value in ["+", "-", "*", "/", "%"]

def _priority(token: Token):
    if token.value == "+":
        return 1
    elif token.value == "-":
        return 1
    elif token.value == "*":
        return 2
    elif token.value == "/":
        return 2
    elif token.value == "%":
        return 2
    return 0

def _is_unary(token: Token):
    return token.value in ["+", "-"]
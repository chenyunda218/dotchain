from ast import Expression
from runtime.ast import BinaryExpression, BoolLiteral, CallExpression, EmptyStatement, FloatLiteral, Fun, Identifier, IntLiteral, Program, Statement, StringLiteral, UnaryExpression, VariableDeclaration
from .tokenizer import Token, TokenType, Tokenizer

unary_prev_statement = [
    TokenType.COMMENTS,
    TokenType.LEFT_PAREN,
    TokenType.COMMA,
    TokenType.LEFT_BRACE,
    TokenType.RIGHT_BRACE,
    TokenType.SEMICOLON,
    TokenType.LET,
    TokenType.RETURN,
    TokenType.IF,
    TokenType.ELSE,
    TokenType.WHILE,
    TokenType.FOR,
    TokenType.LOGICAL_OPERATOR,
    TokenType.NOT,
    TokenType.ASSIGNMENT,
    TokenType.MULTIPLICATIVE_OPERATOR,
    TokenType.ADDITIVE_OPERATOR,
    TokenType.ARROW,
]

end_statement = [
    TokenType.SEMICOLON,
    TokenType.COMMA,
    TokenType.ARROW,
    TokenType.RETURN,
    TokenType.IF,
    TokenType.ELSE,
    TokenType.WHILE,
    TokenType.FOR,
    TokenType.LOGICAL_OPERATOR,
    TokenType.ASSIGNMENT,
    TokenType.RIGHT_BRACE,
]

class ExpressionParser:

    def __init__(self, tkr: Tokenizer):
        self.stack = list[Expression | Token]()
        self.operator_stack = list[Token]()
        self.tkr = tkr

    def parse(self):
        while not self.is_end():
            token = self.tkr.token()
            if self._is_operator(token) or token.type in[TokenType.LEFT_PAREN, TokenType.RIGHT_PAREN ]:
                self.push_operator_stack(token)
                self.tkr.next()
            else:
                self.push_stack(self.expression_parser())
        self.pop_all()
        return self.expression()
    
    def expression(self, index = 0, results: list[Expression] = [])-> Expression:
        if len(self.stack) == 0:
            return EmptyStatement()
        if len(self.stack) == 1:
            return self.stack[0]
        
    def expression_parser(self):
        token = self.tkr.token()
        if token is None:
            return EmptyStatement()
        expression = None
        if self.is_unary():
            expression = self.unary_expression_parser()
        elif token.type == TokenType.INT:
            self.tkr.eat(TokenType.INT)
            expression = IntLiteral(int(token.value))
        elif token.type == TokenType.FLOAT:
            self.tkr.eat(TokenType.FLOAT)
            expression = FloatLiteral(float(token.value))
        elif token.type == TokenType.STRING:
            self.tkr.eat(TokenType.STRING)
            expression = StringLiteral(token.value[1:-1])
        elif token.type == TokenType.BOOL:
            self.tkr.eat(TokenType.BOOL)
            expression = BoolLiteral(token.value == "true")
        elif token.type == TokenType.IDENTIFIER:
            expression = self.identifier_or_func_call_parser()
        return expression
    
    def _try_fun_expression(self):
        self.tkr.checkpoint_push()
        token = self.tkr.token()
        if token.type != TokenType.LEFT_PAREN:
            self.tkr.checkpoint_push()
            return False
        self.tkr.eat(TokenType.LEFT_PAREN)
        while not self.tkr.type_is(TokenType.RIGHT_PAREN):
            if not self.tkr.type_is(TokenType.IDENTIFIER):
                self.tkr.checkpoint_pop()
                return False
            self.tkr.eat(TokenType.IDENTIFIER)
            if self.tkr.type_is(TokenType.RIGHT_PAREN):
                break
            if not self.tkr.type_is(TokenType.COMMA):
                self.tkr.checkpoint_pop()
                return False
            self.tkr.eat(TokenType.COMMA)
        self.tkr.eat(TokenType.RIGHT_PAREN)
        if not self.tkr.type_is(TokenType.ARROW):
            self.tkr.checkpoint_pop()
            return False
        self.tkr.eat(TokenType.ARROW)
        self.tkr.checkpoint_push()
        return True
    
    def push_stack(self, expression: Expression | Token):
        self.stack.append(expression)

    def _pop_by_right_paren(self):
        token = self.operator_stack.pop()
        if token.type != TokenType.LEFT_PAREN:
            self.push_stack(token)
            self._pop_by_right_paren()

    def pop(self):
        self.push_stack(self.operator_stack.pop())

    def pop_all(self):
        while len(self.operator_stack) > 0:
            self.pop()
        for expression in self.stack:
            print(expression)

    def push_operator_stack(self, token: Token):
        if len(self.operator_stack) == 0:
            self.operator_stack.append(token)
            return
        if token.type == TokenType.LEFT_PAREN:
            self.operator_stack.append(token)
            return
        if token.type == TokenType.RIGHT_PAREN:
            self._pop_by_right_paren()
            return
        top_operator = self.operator_stack[-1]
        if top_operator.type == TokenType.LEFT_PAREN:
            self.operator_stack.append(token)
            return
        # priority is in descending order
        if self._priority(token) >= self._priority(top_operator):
            self.pop()
            self.push_operator_stack(token)
            return
        self.operator_stack.append(token)

    def unary_expression_parser(self):
        token = self.tkr.token()
        self.tkr.next()
        return UnaryExpression(token.value, ExpressionParser(self.tkr).parse())

    def identifier_or_func_call_parser(self):
        id = self.identifier()
        tokenType = self.tkr.tokenType()
        if tokenType == TokenType.LEFT_PAREN:
            return self.func_call_parser(id)
        return id
    
    def func_call_parser(self, id: Identifier):
        self.tkr.eat(TokenType.LEFT_PAREN)
        args = list[Expression]()
        while not self.tkr.type_is(TokenType.RIGHT_PAREN):
            args.append(self.expression_parser())
            if self.tkr.type_is(TokenType.COMMA):
                self.tkr.eat(TokenType.COMMA)
        self.tkr.eat(TokenType.RIGHT_PAREN)
        return CallExpression(id, args)

    def identifier(self):
        token = self.tkr.token()
        if token.type != TokenType.IDENTIFIER:
            raise Exception("Invalid identifier", token)
        self.tkr.next()
        return Identifier(token.value)

    def is_unary(self):
        token = self.tkr.token()
        if not self.unary_operator(token):
            return False
        if token.type == TokenType.NOT:
            return True
        prev_token = self.tkr.get_prev()
        if prev_token is None:
            return True
        if prev_token.type == TokenType.LEFT_PAREN:
            return True
        if prev_token.type in unary_prev_statement:
            return True
        return False
    
    def unary_operator(self, token: Token):
        if token is None:
            return False
        return token.value in ["+", "-", "!"]

    def _has_brackets(self):
        return TokenType.LEFT_PAREN in map(lambda x: x.type, self.operator_stack)

    def is_end(self):
        token = self.tkr.token()
        if token is None:
            return True
        if token.type == TokenType.SEMICOLON:
            self.tkr.eat(TokenType.SEMICOLON)
            return True
        if not self._has_brackets() and token.type == TokenType.RIGHT_PAREN:
            return True
        if token.type in end_statement:
            return True
        return False
    
    def _is_operator(self, token: Token):
        if token is None:
            return False
        return token.type in [TokenType.ADDITIVE_OPERATOR, TokenType.MULTIPLICATIVE_OPERATOR]
    
    def _debug_print_tokens(self):
        print("operator stack:----")
        for token in self.operator_stack:
            print(token)

    def _debug_print_stack(self):
        print("stack:----")
        for expression in self.stack:
            print(expression)
    
    def _priority(self, token: Token):
        return _priority(token.value)


def _priority(operator: str):
    priority = 0
    if operator in ["*", "/", "%"]:
        return priority
    priority += 1
    if operator in ["+", "-"]:
        return priority
    priority += 1
    if operator in ["<", ">", "<=", ">="]:
        return priority
    priority += 1
    if operator in ["==", "!="]:
        return priority
    priority += 1
    if operator in ["&&"]:
        return priority
    priority += 1
    if operator in ["||"]:
        return priority
    priority += 1
    return priority
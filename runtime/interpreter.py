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

def statement_parser(tkr: Tokenizer):
    token = tkr.get_current_token()
    
def expression_parser(tkr: Tokenizer)-> Expression:
    token = tkr.get_current_token()
    expression = None
    if token.type == "INT":
        expression = int_literal(tkr)
    elif token.type == "FLOAT":
        expression = float_literal(tkr)
    elif token.type == "STRING":
        expression = string_literal(tkr)
    elif token.type == "BOOL":
        expression = bool_literal(tkr)
    elif token.type == "IDENTIFIER":
        expression = identifier_or_func_call_parser(tkr)
    # TODO: Implement unary expression
    # TODO: Implement function declaration
    if expression is None and tkr.type_is("("):
        return ExpressionStack(tkr).parse()
    token = tkr.get_current_token()
    if token is None or token.value == ";":
        return expression
    if token.value not in ["+", "-", "*", "/", "%"]:
        return expression
    if expression is None:
        raise Exception("Invalid expression", token)
    stack = ExpressionStack(tkr)
    stack.push_expression(expression)
    return stack.parse()


    
def identifier_or_func_call_parser(tkr: Tokenizer) -> Identifier:
    token = tkr.eat(identifier_string)
    next_token = tkr.get_current_token()
    if next_token is not None and next_token.value == "(":
        return func_call_parser(tkr, token)
    return Identifier(token.value)

def func_call_parser(tkr: Tokenizer, id: Identifier):
    tkr.eat("(")
    args = list[Expression]()
    while not tkr.type_is(")"):
        args.append(expression_parser(tkr))
        if tkr.type_is(","):
            tkr.eat(",")
    tkr.eat(")")
    return CallExpression(id, args)

def literal_parser(tkr: Tokenizer):
    token = tkr.get_current_token()
    if token.type == "INT":
        return int_literal(tkr)
    elif token.type == "FLOAT":
        return float_literal(tkr)
    elif token.type == "STRING":
        return string_literal(tkr)
    elif token.type == "BOOL":
        return bool_literal(tkr)
    raise Exception("Invalid literal")

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
def try_fun(tkr: Tokenizer):
    tkr = tkr.clone()
    tkr.eat("(")
    while not tkr.type_is(")"):
        if not tkr.type_is(identifier_string):
            return False
        tkr.eat(identifier_string)
        if tkr.type_is(")"):
            break
        if not tkr.type_is(","):
            return False
        tkr.eat(",")
    try:
        tkr.eat(")")
        tkr.eat("=>")
    except:
        return False
    return True

def fun_parser(tkr: Tokenizer):
    tkr.eat("(")
    args = list[Identifier]()
    while not tkr.type_is(")"):
        if not tkr.type_is(identifier_string):
            raise Exception("Invalid function declaration", token)
        token = tkr.eat(identifier_string)
        args.append(Identifier(token.value))
        if tkr.type_is(")"):
            break
        if not tkr.type_is(","):
            raise Exception("Invalid function declaration", token)
        tkr.eat(",")
    try:
        tkr.eat(")")
        tkr.eat("=>")
    except:
        raise Exception("Invalid function declaration", token)
    # return Fun(args, Block)

class ExpressionParser:

    def __init__(self, tkr: Tokenizer):
        self.stack = list[Expression | Token]()
        self.operator_stack = list[Token]()
        self.tkr = tkr

    def parse(self):
        while not self.is_end():
            token = self.tkr.token()
            if token.type == TokenType.LEFT_PAREN:
                self.push_operator_stack(token)
                self.tkr.next()
            elif self._is_operator(token):
                self.push_operator_stack(token)
                self.tkr.next()
            else:
                self.push_stack(self.expression_parser())
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
        token = self.operator_stack.pop()
        self.push_stack(token)
        return token

    def push_operator_stack(self, token: Token):
        if token.type == TokenType.LEFT_PAREN:
            self.operator_stack.append(token)
            return
        if token.type == TokenType.RIGHT_PAREN:
            self._pop_by_right_paren()
            return
        if len(self.operator_stack) == 0:
            self.operator_stack.append(token)
            return
        

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
        print("tokens:----")
        for token in self.operator_stack:
            print(token)

    def _debug_print_stack(self):
        print("stack:----")
        for expression in self.stack:
            print(expression)

class ExpressionStack:
        
    def __init__(self, tkr: Tokenizer):
        self.stack = list[Expression | Token]()
        self.tokens = list[Token]()
        self.tkr = tkr

    def parse(self):
        while not self._end():
            self.push()
        self.pop_all_tokens()
        return self.expression()
    
    def expression(self, index = 0, results: list[Expression] = [])-> Expression:
        if len(self.stack) == 1:
            return self.stack[0]

    def push(self):
        token = self.tkr.get_current_token()
        if self._is_operator(token):
            self.push_token_and_progress(token)
            self.tkr.get_next_token()
        else:
            self.push_expression(expression_parser(self.tkr))

    def push_expression(self, expression: Expression):
        self.stack.append(expression)
    
    def push_token(self, token: Token):
        self.tokens.append(token)

    def push_token_and_progress(self, token: Token):
        if len(self.tokens) == 0:
            self.tokens.append(token)
            return
        if token.value == "(":
            self.tokens.append(token)
            return
        if token.value == ")":
            self.pop_by_brackets()
            return
        if self.top_token_propity() < self._propity(token):
            self.tokens.append(token)
            return
        while self.top_token_propity() >= self._propity(token):
            self.pop()
            if len(self.tokens) == 0:
                break
        self.tokens.append(token)
            
    def pop(self):
        pop = self.tokens.pop()
        self.stack.append(pop)
        return pop
    
    def pop_all_tokens(self):
        while len(self.tokens) > 0:
            self.pop()
    
    def pop_by_brackets(self):
        token = self.tokens.pop()
        while token.value != "(":
            self.stack.append(token)
            token = self.tokens.pop()
    
    def top(self):
        return self.stack[-1]

    def top_token(self):
        return self.tokens[-1]
    
    def top_token_propity(self):
        if len(self.tokens) == 0:
            return 0
        return self._propity(self.top_token())
    
    def expression(self, index = 0, results: list[Expression] = [])-> Expression:
        if len(self.stack) == 1:
            return self.stack[0]
        if index == len(self.stack):
            return results[0]
        token = self.stack[index]
        if isinstance(token, Token):
            right = results.pop()
            left = results.pop()
            return self.expression(index + 1, results + [BinaryExpression(left, token.value, right)])
        return self.expression(index + 1, results + [token])
        

    def _end(self):
        if self.tkr.get_current_token() is None:
            return True
        if self.tkr.get_current_token().value == ";":
            self.tkr.eat(";")
            return True
        if not self._has_brackets() and self.tkr.get_current_token().value == ")":
            return True
        return False
    
    def _has_brackets(self):
        return "(" in map(lambda x: x.type, self.tokens)

    def _is_operator(self, token: Token):
        if token is None:
            return False
        return token.value in ["+", "-", "*", "/", "%", "(", ")"]
    
    def _propity(self, token: Token):
        if token.value in ["*", "/", "%"]:
            return 2
        if token.value in ["+", "-"]:
            return 1
        return 0

    def _debug_print_tokens(self):
        print("tokens:----")
        for token in self.tokens:
            print(token)

    def _debug_print_stack(self):
        print("stack:----")
        for expression in self.stack:
            print(expression)


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
    return priority
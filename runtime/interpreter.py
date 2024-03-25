from ast import Expression
from runtime.ast import Assignment, BoolLiteral, CallExpression, EmptyStatement, FloatLiteral, Fun, Identifier, IntLiteral, Program, Statement, StringLiteral, UnaryExpression, VariableDeclaration
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
        elif _is_unary(self._get_token()):
            return self.unary_expression()
        if tokenType == ";":
            self.tkr.eat(";")
            return EmptyStatement()
        return EmptyStatement()
    
    def unary_expression(self):
        return UnaryExpression("+", BoolLiteral(False))
    
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
    elif token.value in ["+", "-", "!"]:
        expression = unary_expression_parser(tkr)
    # TODO: Implement function declaration
    if expression is None and tkr.type_is("("):
        print("good")
    token = tkr.get_current_token()
    if token is None or token.value == ";":
        return expression
    if token.value not in ["+", "-", "*", "/", "%"]:
        return expression
    
    return expression
    # raise Exception("Invalid expression", expression)

def binary_expression_helper(tkr: Tokenizer, first: Expression):
    stack = ExpressionStack()
    stack.push(first)
    stack = [first]
    operator_stack = list[Token]()
    while True:
        token = tkr.get_current_token()
        if token is None:
            break
        if token.value == ";":
            tkr.eat(";")
            break
        if _is_operator(token):
            operator_stack.append(token)
        tkr.get_next_token()
    print(token)
    
    
def unary_expression_parser(tkr: Tokenizer):
    token = tkr.get_current_token()
    if token.value in ["+", "-", "!"]:
        tkr.eat(token.type)
        return UnaryExpression(token.value, expression_parser(tkr))
    raise Exception("Invalid unary expression")
    
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

def identifier(tkr: Tokenizer):
    token = tkr.get_current_token()
    tkr.eat(identifier_string)
    return Identifier(token.value)

def let_parser(tkr: Tokenizer):
    tkr.eat("let")
    id = identifier(tkr)
    tkr.eat("=")
    expression = expression(tkr)
    return VariableDeclaration(id, expression)

def _is_unary(token: Token):
    return token.value in ["+", "-"]

def _is_operator(token: Token):
    return token.value in ["+", "-", "*", "/", "%", "(", ")"]

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

class ExpressionStack:
        
        def __init__(self, tkr: Tokenizer):
            self.stack = list[Expression | Token]()
            self.tokens = list[Token]()
            self.tkr = tkr

        def parse(self):
            while not self._end():
                self.push()
            self.pop_all_tokens()
            return self.expression(self.stack)

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
        
        def expression(self, stack: list[Expression | Token] = [], results: list[Expression] = []):
            for expression in stack:
                print(expression)

        def _end(self):
            if self.tkr.get_current_token() is None:
                return True
            if self.tkr.get_current_token().value == ";":
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
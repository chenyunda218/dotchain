import re
from enum import Enum

from attr import dataclass

class TokenType(Enum):
    NEW_LINE = 1
    SPACE = 2
    COMMENTS = 3
    LEFT_PAREN = 4
    RIGHT_PAREN = 5
    COMMA = 6
    LEFT_BRACE = 7
    RIGHT_BRACE = 8
    SEMICOLON = 9
    LET = 10
    RETURN = 11
    IF = 12
    ELSE = 13
    WHILE = 14
    FOR = 15
    TRUE = 16
    FALSE = 17
    FLOAT = 18
    INT = 19
    IDENTIFIER = 20
    LOGICAL_OPERATOR = 21
    NOT = 22
    ASSIGNMENT = 23
    MULTIPLICATIVE_OPERATOR = 24
    ADDITIVE_OPERATOR = 25
    STRING = 26
    ARROW = 27
    BOOL = 28

specs = (
    (re.compile(r"^\n"),TokenType.NEW_LINE),
    # Space:
    (re.compile(r"^\s"),TokenType.SPACE),
    # Comments:
    (re.compile(r"^//.*"), TokenType.COMMENTS),

    # Symbols:
    (re.compile(r"^\("), TokenType.LEFT_PAREN),
    (re.compile(r"^\)"), TokenType.RIGHT_PAREN),
    (re.compile(r"^\,"), TokenType.COMMA),
    (re.compile(r"^\{"), TokenType.LEFT_BRACE),
    (re.compile(r"^\}"), TokenType.RIGHT_BRACE),
    (re.compile(r"^;"), TokenType.SEMICOLON),
    (re.compile(r"^=>"), TokenType.ARROW),

    # Keywords:
    (re.compile(r"^\blet\b"), TokenType.LET),
    (re.compile(r"^\breturn\b"), TokenType.RETURN),
    (re.compile(r"^\bif\b"), TokenType.IF),
    (re.compile(r"^\belse\b"), TokenType.ELSE),
    (re.compile(r"^\bwhile\b"), TokenType.WHILE),
    (re.compile(r"^\bfor\b"), TokenType.FOR),

    (re.compile(r"^\btrue\b"), TokenType.BOOL),
    (re.compile(r"^\bfalse\b"), TokenType.BOOL),


    # Floats:
    (re.compile(r"^[0-9]+\.[0-9]+"), TokenType.FLOAT),

    # Ints:
    (re.compile(r"^[0-9]+"), TokenType.INT),

    # Identifiers:
    (re.compile(r"^\w+"),  TokenType.IDENTIFIER),


    # Logical operators:
    (re.compile(r"^&&"),  TokenType.LOGICAL_OPERATOR),
    (re.compile(r"^\|\|"), TokenType.LOGICAL_OPERATOR),
    (re.compile(r"^=="), TokenType.LOGICAL_OPERATOR),
    (re.compile(r"^!="), TokenType.LOGICAL_OPERATOR),
    (re.compile(r"^<="), TokenType.LOGICAL_OPERATOR),
    (re.compile(r"^>="), TokenType.LOGICAL_OPERATOR),
    (re.compile(r"^<"), TokenType.LOGICAL_OPERATOR),
    (re.compile(r"^>"), TokenType.LOGICAL_OPERATOR),

    (re.compile(r"^!"), TokenType.NOT),

    # Assignment:
    (re.compile(r"^="), TokenType.ASSIGNMENT),

    # Math operators: +, -, *, /:
    (re.compile(r"^[*/%]"), TokenType.MULTIPLICATIVE_OPERATOR),
    (re.compile(r"^[+-]"), TokenType.ADDITIVE_OPERATOR),

    # Double-quoted strings
    (re.compile(r"^\"[^\"]*\""), TokenType.STRING),
)

@dataclass
class Token:
    type: str
    value: str
    row: int
    col: int
    col_end: int
    cursor: int
    
    def __str__(self) -> str:
        return f"Token({self.type}, {self.value}, row={self.row}, col={self.col}, col_end={self.col_end}, cursor={self.cursor})"


class Tokenizer:

    def __init__(self):
        self._current_token = None
        self.script = ""
        self.cursor = 0
        self.col = 0
        self.row = 0
        self._current_token_index = 0
        self.tokens = list[Token]()
    
    def init(self, script: str):
        self.tokens = list[Token]()
        self._current_token_index = 0
        self._current_token = None
        self.script = script
        self.cursor = 0
        self.col = 0
        self.row = 0
        self._get_next_token()
        while self._current_token is not None:
            self.tokens.append(self._current_token)
            self._get_next_token()
    
    def next(self):
        self._current_token_index += 1
        return self.token()
    
    def prev(self):
        self._current_token_index -= 1
        return self.token()
    
    def get_prev(self):
        if self._current_token_index == 0:
            return None
        return self.tokens[self._current_token_index - 1]
    
    def get_next(self):
        if self._current_token_index >= len(self.tokens):
            return None
        return self.tokens[self._current_token_index + 1]

    def token(self):
        if self._current_token_index >= len(self.tokens):
            return None
        return self.tokens[self._current_token_index]

    def _get_next_token(self):
        if self._is_eof():
            self._current_token = None
            return None
        _string = self.script[self.cursor:]
        for spec in specs:
            tokenValue, offset = self.match(spec[0], _string)
            if tokenValue == None:
                continue
            if (spec[1] == TokenType.NEW_LINE or spec[1] == TokenType.COMMENTS):
                self.row += 1
                self.col = 0
                return self._get_next_token()
            if (spec[1] == TokenType.SPACE):
                self.col += offset
                return self._get_next_token()
            if (spec[1] == None):
                return self._get_next_token()
            self._current_token = Token(spec[1],tokenValue, self.cursor, self.row, self.col, self.col + offset)
            self.col += offset
            return self.get_current_token()
        raise Exception("Unknown token: " + _string[0])

    def init_and_next(self,script: str):
        self.init(script)
        return self._get_next_token()

    def _is_eof(self):
        return self.cursor == len(self.script)
    
    def has_more_tokens(self):
        return self.cursor < len(self.script)

    def type_is(self, tokenType: str):
        if self._current_token == None:
            return False
        return self._current_token.type == tokenType

    def get_current_token(self):
        return self._current_token
    
    def match(self, reg: re, _script):
        matched = reg.search(_script)
        if matched == None:
            return None,0
        self.cursor = self.cursor + matched.span(0)[1]
        return matched[0], matched.span(0)[1]
    
    def token_list(self):
        tokens = []
        tokenizer = self.clone()
        token = tokenizer._get_next_token()
        while token is not None:
            tokens.append(token)
            token = tokenizer._get_next_token()
        return tokens

    def token_list(self):
        tokens = []
        tokenizer = self.clone()
        token = tokenizer._get_next_token()
        while token is not None:
            tokens.append(token)
            token = tokenizer._get_next_token()
        return tokens

    def eat(self, tokenType: str) -> Token:
        token = self.get_current_token()
        if token == None:
            raise Exception("Unexpected EOF")
        if token.type != tokenType:
            raise Exception("Unexpected token: {} != {}".format(token.type, tokenType))
        self._get_next_token()
        return token
    
    def copy(self, tokenizer):
        self._current_token = tokenizer._current_token
        self.script = tokenizer.script
        self.cursor = tokenizer.cursor
        self.col = tokenizer.col
        self.row = tokenizer.row

    def clone(self):
        t = Tokenizer()
        t.copy(self)
        return t
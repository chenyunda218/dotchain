import re

specs = (
    (re.compile(r"^\n"), "NEW_LINE"),
    # Space:
    (re.compile(r"^\s"), "SPACE"),
    # Comments:
    (re.compile(r"^//.*"), "COMMENTS"),

    # Symbols:
    (re.compile(r"^\("), "("),
    (re.compile(r"^\)"), ")"),
    (re.compile(r"^\,"), ","),
    (re.compile(r"^\{"), "{"),
    (re.compile(r"^\}"), "}"),
    (re.compile(r"^;"), ";"),
    (re.compile(r"^=>"), "=>"),

    # Keywords:
    (re.compile(r"^\blet\b"), "let"),
    (re.compile(r"^\breturn\b"), "return"),
    (re.compile(r"^\bif\b"), "if"),
    (re.compile(r"^\belse\b"), "else"),
    (re.compile(r"^\bwhile\b"), "while"),
    (re.compile(r"^\bfor\b"), "for"),

    (re.compile(r"^\btrue\b"), "BOOL"),
    (re.compile(r"^\bfalse\b"), "BOOL"),


    # Floats:
    (re.compile(r"^[0-9]+\.[0-9]+"), "FLOAT"),

    # Ints:
    (re.compile(r"^[0-9]+"), "INT"),

    # Identifiers:
    (re.compile(r"^\w+"), "IDENTIFIER"),

    # Assignment:
    (re.compile(r"^="), "="),

    # Logical operators:
    (re.compile(r"^&&"), "LOGICAL_OPERATOR"),
    (re.compile(r"^\|\|"), "LOGICAL_OPERATOR"),
    (re.compile(r"^=="), "LOGICAL_OPERATOR"),
    (re.compile(r"^!="), "LOGICAL_OPERATOR"),
    (re.compile(r"^<"), "LOGICAL_OPERATOR"),
    (re.compile(r"^>"), "LOGICAL_OPERATOR"),
    (re.compile(r"^<="), "LOGICAL_OPERATOR"),
    (re.compile(r"^>="), "LOGICAL_OPERATOR"),

    (re.compile(r"^!"), "NOT"),

    # Math operators: +, -, *, /:
    (re.compile(r"^[*/]"), "MATH_OPERATORS"),
    (re.compile(r"^[+-]"), "MATH_OPERATORS"),

    # Double-quoted strings
    (re.compile(r"^\"[^\"]*\""), "STRING"),
)

class Token:
    
    def __init__(self, type: str, value: str, cursor = 0, row = 0, col = 0, col_end = 0) -> None:
        self.type = type
        self.value = value
        self.row = row
        self.col = col
        self.col_end = col_end
        self.cursor = cursor

    def __str__(self) -> str:
        return f"Token({self.type}, {self.value}, row={self.row}, col={self.col}, col_end={self.col_end}, cursor={self.cursor})"


class Tokenizer:

    def __init__(self):
        self.current_token = None
        self.script = ""
        self.cursor = 0
        self.col = 0
        self.row = 0
    
    def init(self, script: str):
        self.script = script
        self.cursor = 0
        self.col = 0
        self.row = 0

    def isEOF(self):
        return self.cursor == len(self.script)
    
    def has_more_tokens(self):
        return self.cursor < len(self.script)

    def get_current_token(self):
        return self.current_token

    def get_next_token(self):
        if self.isEOF():
            self.current_token = None
            return None
        _string = self.script[self.cursor:]
        for spec in specs:
            tokenValue, offset = self.match(spec[0], _string)
            if tokenValue == None:
                continue
            if (spec[1] == "NEW_LINE" or spec[1] == "COMMENTS"):
                self.row += 1
                self.col = 0
                return self.get_next_token()
            if (spec[1] == "SPACE"):
                self.col += offset
                return self.get_next_token()
            if (spec[1] == None):
                return self.get_next_token()
            self.current_token = Token(spec[1],tokenValue, self.cursor, self.row, self.col, self.col + offset)
            self.col += offset
            return self.get_current_token()
        raise Exception("Unknown token: " + _string[0])
    
    def match(self, reg: re, _script):
        matched = reg.search(_script)
        if matched == None:
            return None,0
        self.cursor = self.cursor + matched.span(0)[1]
        return matched[0], matched.span(0)[1]
    
    def token_list(self):
        tokens = []
        tokenizer = self.clone()
        token = tokenizer.get_next_token()
        while token is not None:
            tokens.append(token)
            token = tokenizer.get_next_token()
        return tokens

    def clone(self):
        t = Tokenizer()
        t.script = self.script
        t.cursor = self.cursor
        t.current_token = self.current_token
        return t

    def eat(self, tokenType: str) -> Token:
        token = self.get_current_token()
        if token == None:
            raise Exception("Unexpected EOF")
        if token.type != tokenType:
            raise Exception("Unexpected token: " + token.type)
        self.get_next_token()
        return token
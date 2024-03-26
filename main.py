from runtime.ast import BinaryExpression, Expression
from runtime.interpreter import ExpressionParser, block_expression, let_expression_parser, program_parser
from runtime.runtime import Runtime
from runtime.tokenizer import TokenType, Tokenizer, Token
import json

script = """

let good = 123;
whereareyou = 10;
hello = 12312 + 123 - -hello();
hello();
"""



if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    parser = program_parser(t)
    json_object = json.dumps(parser.dict())
    print(json_object)
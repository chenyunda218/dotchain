from runtime.ast import BinaryExpression, Expression
from runtime.interpreter import ExpressionParser, block_expression, let_expression_parser
from runtime.runtime import Runtime
from runtime.tokenizer import TokenType, Tokenizer, Token
import json

script = """
{
    let a = hello + -3 / -4;
    let b = -hello() + 3 / -4;
}
"""



if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    parser = block_expression(t)
    json_object = json.dumps(parser.dict())
    print(json_object)
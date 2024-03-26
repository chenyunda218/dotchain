from runtime.ast import BinaryExpression, Expression
from runtime.interpreter import ExpressionParser
from runtime.runtime import Runtime
from runtime.tokenizer import TokenType, Tokenizer, Token
import json

script = """
9+(3-1)*3+10/2;
"""

def expression_list_to_binary(expression_list: list[Expression], stack = list[Expression]):
    if len(expression_list) == 1:
        return expression_list[0]
    if len(expression_list) == 2:
        return BinaryExpression(expression_list[0], expression_list[1], stack.pop())
    else:
        return expression_list_to_binary([BinaryExpression(expression_list[0], expression_list[1], stack.pop())] + expression_list[2:], stack)
    

if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    parser = ExpressionParser(t)
    # parser.push_token(Token(TokenType.LEFT_PAREN, "(", 0, 0, 1, 0))
    expression = parser.parse()
    # print(expression.dict())
    for e in expression:
        print(e)


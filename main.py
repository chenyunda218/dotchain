

from runtime.interpreter import ExpressionStack, expression_parser
from runtime.runtime import Runtime
from runtime.tokenizer import Tokenizer
import json

script = """
(;
"""

binary_script = """
1 + 2 * 4;
"""

if __name__ == "__main__":
    # t = Tokenizer()
    # t.init(script)
    # t.get_next_token()
    # u = expression_parser(t)
    # print(u)
    tkr = Tokenizer()
    tkr.init_and_next("a + 9 + ( 3 - 1 ) * 3 + 10 / 2;")
    expression = expression_parser(tkr)
    
    
    # print(binary)
    json_object = json.dumps(expression.dict()) 

    # Print JSON object
    print(json_object) 


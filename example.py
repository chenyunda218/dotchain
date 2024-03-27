

import json
from runtime.interpreter import ExpressionParser
from runtime.tokenizer import Tokenizer


script = """
234 == 1234 && 412 <= 123
"""

if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    ast = ExpressionParser(t).parse()
    json_object = json.dumps(ast.dict()) 
    print(json_object) 
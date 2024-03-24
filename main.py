

from runtime.interpreter import Interpreter, binary_expression
from runtime.parser import Parser
from runtime.runtime import Runtime
from runtime.tokenizer import Tokenizer
import json

script = """
let hello = 123;
"""

binary_script = """
1 + 2 * 4;
"""

if __name__ == "__main__":
    # t = Tokenizer()
    # t.init(binary_script)
    # out = binary_expression(t.token_list())
    # for o in out:
    #     print(o)
    interpreter = Interpreter()
    ast = interpreter.parse(script)
    print(ast)
    # env = Runtime()
    # env.run(ast)
    # env.context.show_values()
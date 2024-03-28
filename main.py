
from runtime.interpreter import program_parser
from runtime.runtime import Runtime, exec_program
from runtime.tokenizer import Tokenizer
import json

script = """
print("hello", "world");
"""
if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    runtime = Runtime(exteral_fun={"print": print})
    ast = program_parser(t)
    json_object = json.dumps(ast.dict()) 
    print(json_object)
    exec_program(runtime, ast)
    runtime.show_values()
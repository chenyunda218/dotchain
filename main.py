
from runtime.interpreter import program_parser
from runtime.program_runtime import ProgrameRuntime
from runtime.tokenizer import Tokenizer
import json

script = """
let hello = 123;
hello = 456;

"""

if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    runtime = ProgrameRuntime()
    ast = program_parser(t)
    json_object = json.dumps(ast.dict()) 
    print(json_object)
    print()
    runtime.exec(ast)
    runtime.show_values()

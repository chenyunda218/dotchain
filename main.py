
from runtime.interpreter import program_parser
from runtime.runtime import Runtime, exec_program
from runtime.tokenizer import Tokenizer
import json

script = """
let a = world((a, b ) => {
    print("labmda called");
    return 1 + 2 * 4;
});

return 200;

"""

if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    runtime = Runtime(exteral_fun={"print": print})
    ast = program_parser(t)
    json_object = json.dumps(ast.dict()) 
    print(json_object)
    result = exec_program(runtime, ast)
    print(result)
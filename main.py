
from runtime.interpreter import program_parser
from runtime.runtime import Runtime, exec_statement
from runtime.tokenizer import Tokenizer
import json

script = """
let hello = () => {
    print("Hello World");
}
world();
print("hell");
"""

if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    runtime = Runtime(exteral_fun={"print": print})
    ast = program_parser(t)
    json_object = json.dumps(ast.dict()) 
    print(json_object)

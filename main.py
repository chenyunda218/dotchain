
from runtime.interpreter import program_parser
from runtime.ast import Runtime
from runtime.program_runtime import ProgrameRuntime
from runtime.tokenizer import Tokenizer
import json

script = """
let hello = () => {
    while a == b {
        print("hello")
        if a == b {
            print("hello");
        } else {
            print("world");
            break;
        }
        return hello() + 4;
    }
}
"""



if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    runtime = ProgrameRuntime()
    ast = program_parser(t)
    json_object = json.dumps(ast.dict()) 
    print(json_object)
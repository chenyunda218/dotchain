
from runtime.interpreter import program_parser
from runtime.runtime import Runtime
from runtime.tokenizer import Tokenizer
import json

script = """
let c = 123 + 123;
if c < 100 {
    print("Hello, World!");
} else {
    print("Goodbye, World!");
}
"""

if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    runtime = Runtime(exteral_fun={"print": print})
    ast = program_parser(t)
    result = ast.exec(runtime)
    runtime.show_values()
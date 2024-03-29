
from runtime.interpreter import program_parser
from runtime.runtime import Runtime
from runtime.tokenizer import Tokenizer
import json

script = """
let c = 123 + 123;
let hello = (a) => {
    print("hello", a);
}
while c > 0 {
    let count = 12;
    print("count", count);
    if c < 12 {
        break;
    }
    c = c - 1;
}
hello(123);
"""

if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    runtime = Runtime(exteral_fun={"print": print})
    ast = program_parser(t)
    result = ast.exec(runtime)
    runtime.show_values()

from runtime.interpreter import program_parser
from runtime.ast import Runtime
from runtime.program_runtime import ProgrameRuntime
from runtime.tokenizer import Tokenizer
import json

script = """
let hello = 1 + 2 / 4;
"""



if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    runtime = ProgrameRuntime()
    runtime.exec(program_parser(t))
    runtime.show_values()
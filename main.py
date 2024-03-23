
from runtime.parser import Parser
from runtime.tokenizer import Tokenizer
import json

script = """
    let dan = -10 +    100
let c = 20.23
"""

if __name__ == "__main__":
    t = Tokenizer()
    t.init(script)
    token_list = t.token_list()
    for token in token_list:
        print(token)
    # p = Parser()
    # pro = p.parse(script)
    # print(pro.dict())
import unittest
from runtime.tokenizer import Tokenizer



class TestTokenizer(unittest.TestCase):

    def test_init(self):
        t = Tokenizer()
        self.assertEqual(t.script, "")
        self.assertEqual(t.cursor, 0)
        self.assertEqual(t.col, 0)
        self.assertEqual(t.row, 0)
        self.assertEqual(t.isEOF(), True)
        self.assertEqual(t.get_current_token(), None)
    
    def test_init_script(self):
        test_script = """
        let hello = 123;
        """
        t = Tokenizer()
        t.init(test_script)
        self.assertEqual(len(t.token_list()), 5)

    def test_clone(self):
        t = Tokenizer()
        t.init("let hello = 123;")
        t.get_current_token()
        t2 = t.clone()
        self.assertEqual(t2.script, t.script)
        self.assertEqual(t2.cursor, t.cursor)
        self.assertEqual(t2.col, t.col)
        self.assertEqual(t2.row, t.row)
        self.assertEqual(t2.get_current_token(), t.get_current_token())
        t2.get_next_token()

    def test_get_next_token(self):
        t = Tokenizer()
        t.init("""
               let hello = 123;
               hello = "world";
               good = 123.123 + 123;
               let right = true;
               right = false;
               """)
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "let")
        self.assertEqual(t.get_current_token().value, "let")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "IDENTIFIER")
        self.assertEqual(t.get_current_token().value, "hello")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "=")
        self.assertEqual(t.get_current_token().value, "=")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "INT")
        self.assertEqual(t.get_current_token().value, "123")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, ";")
        self.assertEqual(t.get_current_token().value, ";")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "IDENTIFIER")
        self.assertEqual(t.get_current_token().value, "hello")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "=")
        self.assertEqual(t.get_current_token().value, "=")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "STRING")
        self.assertEqual(t.get_current_token().value, "\"world\"")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, ";")
        self.assertEqual(t.get_current_token().value, ";")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "IDENTIFIER")
        self.assertEqual(t.get_current_token().value, "good")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "=")
        self.assertEqual(t.get_current_token().value, "=")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "FLOAT")
        self.assertEqual(t.get_current_token().value, "123.123")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "ADDITIVE_OPERATOR")
        self.assertEqual(t.get_current_token().value, "+")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "INT")
        self.assertEqual(t.get_current_token().value, "123")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, ";")
        self.assertEqual(t.get_current_token().value, ";")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "let")
        self.assertEqual(t.get_current_token().value, "let")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "IDENTIFIER")
        self.assertEqual(t.get_current_token().value, "right")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "=")
        self.assertEqual(t.get_current_token().value, "=")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "BOOL")
        self.assertEqual(t.get_current_token().value, "true")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, ";")
        self.assertEqual(t.get_current_token().value, ";")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "IDENTIFIER")
        self.assertEqual(t.get_current_token().value, "right")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "=")
        self.assertEqual(t.get_current_token().value, "=")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, "BOOL")
        self.assertEqual(t.get_current_token().value, "false")
        t.get_next_token()
        self.assertEqual(t.get_current_token().type, ";")
        self.assertEqual(t.get_current_token().value, ";")
        t.get_next_token()
        self.assertEqual(t.get_current_token(), None)
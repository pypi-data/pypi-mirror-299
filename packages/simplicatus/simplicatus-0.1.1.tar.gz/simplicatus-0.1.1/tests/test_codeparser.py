import unittest
from simplicatus import say_hello_codeparser

class TestSayHello(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(say_hello_codeparser("Codeparser"), "Hello, Codeparser!")

if __name__ == "__main__":
    unittest.main()




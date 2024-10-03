import unittest
from simplicatus import say_hello

class TestSayHello(unittest.TestCase):
    def test_hello(self):
        self.assertEqual(say_hello("Simparser"), "Hello, Simparser!")

if __name__ == "__main__":
    unittest.main()
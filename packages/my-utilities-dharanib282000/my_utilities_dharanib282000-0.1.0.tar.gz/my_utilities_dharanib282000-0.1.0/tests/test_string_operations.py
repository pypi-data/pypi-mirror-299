import unittest
from my_utilities_dharanib282000.string_operations import capitalize_words, reverse_string, count_vowels

class TestStringOperations(unittest.TestCase):
    def test_capitalize_words(self):
        self.assertEqual(capitalize_words('hello world'), 'Hello World')

    def test_reverse_string(self):
        self.assertEqual(reverse_string('hello'), 'olleh')

    def test_count_vowels(self):
        self.assertEqual(count_vowels('hello'), 2)

if __name__ == '__main__':
    unittest.main()

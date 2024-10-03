import unittest
import os
from my_utilities_dharanib282000.file_operations import read_file, write_file

class TestFileOperations(unittest.TestCase):
    def setUp(self):
        self.test_file = 'test.txt'
        write_file(self.test_file, 'Hello, World!')

    def test_read_file(self):
        content = read_file(self.test_file)
        self.assertEqual(content, 'Hello, World!')

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            read_file('non_existing_file.txt')

    def tearDown(self):
        os.remove(self.test_file)

if __name__ == '__main__':
    unittest.main()

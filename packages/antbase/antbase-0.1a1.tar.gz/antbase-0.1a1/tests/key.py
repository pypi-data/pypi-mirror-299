import unittest
from antbase._.server_base.key import Key

class TestKey(unittest.TestCase):

    def test_encode(self):
        key = {'type': 'D3', 'prefix': 'P-', 'suffix': '-S'}
        self.assertEqual(Key.encode(123, key), 'P-123-S')
        self.assertEqual(Key.encode(999, key), 'P-999-S')
        self.assertIsNone(Key.encode(1000, key))  # Out of range

        key = {'type': 'L3', 'prefix': 'P-', 'suffix': '-S'}
        self.assertEqual(Key.encode(17576, key), 'P-AAA-S')
        self.assertEqual(Key.encode(17577, key), 'P-AAB-S')
        self.assertIsNone(Key.encode(26**3, key))  # Out of range

    def test_decode(self):
        key = {'type': 'D3', 'syntax': r'^\d{3}$'}
        self.assertEqual(Key.decode('123', key), 123)
        self.assertEqual(Key.decode('999', key), 999)
        with self.assertRaises(ValueError):
            Key.decode('1000', key)  # Invalid syntax

        key = {'type': 'L3', 'syntax': r'^[A-Z]{3}$'}
        self.assertEqual(Key.decode('AAA', key), 17576)
        self.assertEqual(Key.decode('AAB', key), 17577)
        with self.assertRaises(ValueError):
            Key.decode('AAAA', key)  # Invalid syntax

    def test_max(self):
        self.assertEqual(Key.max('D3'), 999)
        self.assertEqual(Key.max('L3'), 26**3 - 1)
        self.assertIsNone(Key.max('invalid_type'))

if __name__ == '__main__':
    unittest.main()
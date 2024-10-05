import unittest

from ArmPointer import ArmPointer


class TestPointer(unittest.TestCase):
    class Dummy:
        def __init__(self, value):
            self.value = value

        def increment(self):
            self.value += 1

        def __len__(self):
            return self.value

        def __getitem__(self, key):
            return self.value + key

        def __setitem__(self, key, value):
            self.value = value

        # Implementing arithmetic operations
        def __add__(self, other):
            return self.value + other

        def __sub__(self, other):
            return self.value - other

        def __mul__(self, other):
            return self.value * other

        def __truediv__(self, other):
            return self.value / other

        def __floordiv__(self, other):
            return self.value // other

        def __mod__(self, other):
            return self.value % other

        def __pow__(self, other, modulo=None):
            return pow(self.value, other, modulo)

        def __and__(self, other):
            return self.value & other

        def __or__(self, other):
            return self.value | other

        def __xor__(self, other):
            return self.value ^ other

        def __invert__(self):
            return ~self.value

        def __lshift__(self, other):
            return self.value << other

        def __rshift__(self, other):
            return self.value >> other

        def __lt__(self, other):
            return self.value < other

        def __le__(self, other):
            return self.value <= other

        def __gt__(self, other):
            return self.value > other

        def __ge__(self, other):
            return self.value >= other

    def setUp(self):
        self.dummy = self.Dummy(5)
        self.pointer = ArmPointer(self.dummy)

    def test_initialization(self):
        self.assertIsNotNone(self.pointer)
        self.assertEqual(self.pointer.ptr.value, 5)

    def test_get_attribute(self):
        self.assertEqual(self.pointer.value, 5)

    def test_set_attribute(self):
        self.pointer.value = 10
        self.assertEqual(self.pointer.ptr.value, 10)

    def test_delete_attribute(self):
        self.pointer.value = 10
        del self.pointer.value
        with self.assertRaises(AttributeError):
            _ = self.pointer.value

    def test_call_method(self):
        self.pointer.increment()
        self.assertEqual(self.pointer.ptr.value, 6)

    def test_length(self):
        self.assertEqual(len(self.pointer), 5)
        self.pointer.increment()
        self.assertEqual(len(self.pointer), 6)

    def test_get_item(self):
        self.assertEqual(self.pointer[0], 5)

    def test_set_item(self):
        self.pointer[0] = 10
        self.assertEqual(self.pointer.ptr.value, 10)

    def test_addition(self):
        self.assertEqual(self.pointer + 5, 10)

    def test_subtraction(self):
        self.assertEqual(self.pointer - 2, 3)

    def test_multiplication(self):
        self.assertEqual(self.pointer * 2, 10)

    def test_division(self):
        self.assertEqual(self.pointer / 2, 5.0)

    def test_boolean(self):
        self.assertTrue(self.pointer)
        self.pointer.value = 0
        self.assertFalse(self.pointer)

    def test_equality(self):
        another_pointer = ArmPointer(self.dummy)
        self.assertEqual(self.pointer, another_pointer)

    def test_inequality(self):
        another_dummy = self.Dummy(10)
        another_pointer = ArmPointer(another_dummy)
        self.assertNotEqual(self.pointer, another_pointer)


if __name__ == '__main__':
    unittest.main()

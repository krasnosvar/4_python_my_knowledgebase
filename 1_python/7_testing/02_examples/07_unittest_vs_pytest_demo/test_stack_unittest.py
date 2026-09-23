"""
unittest-стиль: TestCase, setUp/tearDown, assertEqual/assertRaises, subTest.

Запуск: pytest 02_examples/07_unittest_vs_pytest_demo/test_stack_unittest.py
(pytest умеет запускать unittest.TestCase без изменений)
"""
from __future__ import annotations

import unittest

from stack import Stack


class TestStackUnittest(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_push_pop(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(self.stack.pop(), 1)

    def test_pop_empty_raises(self):
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_multiple_values_via_subtest(self):
        cases = [1, "two", 3.0, None]
        for value in cases:
            with self.subTest(value=value):
                self.stack.push(value)
                self.assertEqual(self.stack.pop(), value)


if __name__ == "__main__":
    unittest.main()

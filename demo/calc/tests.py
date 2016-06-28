from django.test import TestCase
from calc.calculator import Calculator
from calc.scalc import SimpleCalculator
from unittest.mock import MagicMock

# Create your tests here.
class TestCalculator(TestCase):

    def setUp(self):
        self.calc = Calculator()

    def test_parseString(self):
        parseString = self.calc.parseString
        self.assertEqual(parseString('0'), ['0'])
        self.assertEqual(parseString('1'), ['1'])
        self.assertEqual(parseString('3+2'), ['3', '2', '+'])

    def test_evalStack(self):
        evalStack = self.calc.evalStack
        self.assertEqual(evalStack(['0']), 0)
        self.assertEqual(evalStack(['1']), 1)

    def test_evalString(self):
        evalString = self.calc.evalString
        self.assertEqual(evalString('0'), 0)
        self.assertEqual(evalString('1'), 1)

    def test_invalid_input(self):
        evalString = self.calc.evalString
        self.assertEqual(evalString('hello world'), 'Invalid Input')

    def test_num_op_num(self):
        evalString = self.calc.evalString
        self.assertEqual(evalString('3+2'), 5)
        self.assertEqual(evalString('3-2'), 1)
        self.assertEqual(evalString('3*2'), 6)
        self.assertEqual(evalString('3/2'), 1.5)
        self.assertEqual(evalString('7+5'), 12)
        self.assertEqual(evalString('7-5'), 2)
        self.assertEqual(evalString('7*5'), 35)
        self.assertEqual(evalString('7/5'), 1.4)

    def test_order_of_operations(self):
        evalString = self.calc.evalString
        self.assertEqual(evalString('4+3*2'), 10)
        self.assertEqual(evalString('9-3*2+2/1'), 5)

    def test_parentheses(self):
        evalString = self.calc.evalString
        self.assertEqual(evalString('(4+3)*2'), 14)
        self.assertEqual(evalString('(9-3)*(2+2)/1'), 24)

    def test_commutative_property(self):
        evalString = self.calc.evalString
        self.assertEqual(evalString('3+4'), evalString('4+3'))
        self.assertEqual(evalString('2*5'), evalString('5*2'))

    def test_associative_property(self):
        evalString = self.calc.evalString
        self.assertEqual(evalString('(5+2) + 1'), evalString('5 + (2+1)'))
        self.assertEqual(evalString('(5*2) * 3'), evalString('5 * (2*3)'))

    def test_distributive_property(self):
        evalString = self.calc.evalString
        self.assertEqual(evalString('2 * (1+3)'), evalString('(2*1) + (2*3)'))
        self.assertEqual(evalString('(1+3) * 2'), evalString('(1*2) + (3*2)'))

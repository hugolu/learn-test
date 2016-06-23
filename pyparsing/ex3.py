from pyparsing import Word, Literal, nums, ZeroOrMore
import unittest

"""
op      :: '+' | '-' | '*' | '/'
atom    :: '0'...'9'+
term    :: atom + [mulop + atom]*
expr    :: term + [addop + term]*
"""

exprStack = []
def pushFirst(s, l, t):
    exprStack.append(t[0])

add = Literal('+')
sub = Literal('-')
mul = Literal('*')
div = Literal('/')
addop = add | sub
mulop = mul | div

atom = Word(nums).addParseAction(pushFirst)
term = atom + ZeroOrMore((mulop + atom).addParseAction(pushFirst))
expr = term + ZeroOrMore((addop + term).addParseAction(pushFirst))

def parseString(string):
    global exprStack
    exprStack = []
    expr.parseString(string)
    return exprStack

opf = { '+' : (lambda a, b: a + b),
        '-' : (lambda a, b: a - b),
        '*' : (lambda a, b: a * b),
        '/' : (lambda a, b: a / b) }

def evalStack(stack):
    op = stack.pop()
    if op in '+-*/':
        op2 = evalStack(stack)
        op1 = evalStack(stack)
        return opf[op](op1, op2)
    else:
        return float(op)

def evalString(string):
    stack = parseString(string)
    result = evalStack(stack)
    return result

class TestEx2(unittest.TestCase):

    def test_parseString(self):
        self.assertEqual(parseString('6+3'), ['6', '3', '+'])
        self.assertEqual(parseString('6-3'), ['6', '3', '-'])
        self.assertEqual(parseString('6*3'), ['6', '3', '*'])
        self.assertEqual(parseString('6/3'), ['6', '3', '/'])

    def test_evalStack(self):
        self.assertEqual(evalStack(['6', '3', '+']), 9.0)
        self.assertEqual(evalStack(['6', '3', '-']), 3.0)
        self.assertEqual(evalStack(['6', '3', '*']), 18.0)
        self.assertEqual(evalStack(['6', '3', '/']), 2.0)

    def test_evalString(self):
        self.assertEqual(evalString('6+3'), 9.0)
        self.assertEqual(evalString('6-3'), 3.0)
        self.assertEqual(evalString('6*3'), 18.0)
        self.assertEqual(evalString('6/3'), 2.0)

    def test_multiple_op(self):
        self.assertEqual(evalString('6+3+2'), 11.0)
        self.assertEqual(evalString('6-3-2'), 1.0)
        self.assertEqual(evalString('6*3*2'), 36.0)
        self.assertEqual(evalString('6/3/2'), 1.0)

    def test_order_of_operations(self):
        self.assertEqual(evalString('2+3*4'), 14.0)
        self.assertEqual(evalString('5+4*3-2/1'), 15.0)

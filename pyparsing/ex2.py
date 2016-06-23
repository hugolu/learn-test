from pyparsing import Word, Literal, nums, ZeroOrMore
import unittest

"""
op      :: '+' | '-' | '*' | '/'
num     :: '0'...'9'+
expr    :: num + op + num
"""

exprStack = []
def pushFirst(s, l, t):
    exprStack.append(t[0])

add = Literal('+')
sub = Literal('-')
mul = Literal('*')
div = Literal('/')
op = add | sub | mul | div

atom = Word(nums).addParseAction(pushFirst)
expr = atom + ZeroOrMore((op + atom).addParseAction(pushFirst))

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


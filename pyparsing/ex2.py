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

def parseString(s):
    global exprStack
    exprStack = []
    expr.parseString(s)
    return exprStack

opf = { '+' : (lambda a, b: a + b),
        '-' : (lambda a, b: a - b),
        '*' : (lambda a, b: a * b),
        '/' : (lambda a, b: a / b) }

def evalStack(s):
    op = s.pop()
    if op in '+-*/':
        op2 = evalStack(s)
        op1 = evalStack(s)
        return opf[op](op1, op2)
    else:
        return float(op)

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

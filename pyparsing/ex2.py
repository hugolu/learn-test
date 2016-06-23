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

def evalString(s):
    global exprStack
    exprStack = []
    expr.parseString(s)
    return exprStack

class TestEx2(unittest.TestCase):

    def test_single_op(self):
        self.assertEqual(evalString('6+3'), ['6', '3', '+'])
        self.assertEqual(evalString('6-3'), ['6', '3', '-'])
        self.assertEqual(evalString('6*3'), ['6', '3', '*'])
        self.assertEqual(evalString('6/3'), ['6', '3', '/'])

    def test_multiple_op(self):
        self.assertEqual(evalString('6+3+2'), ['6', '3', '+', '2', '+'])
        self.assertEqual(evalString('6-3-2'), ['6', '3', '-', '2', '-'])
        self.assertEqual(evalString('6*3*2'), ['6', '3', '*', '2', '*'])
        self.assertEqual(evalString('6/3/2'), ['6', '3', '/', '2', '/'])


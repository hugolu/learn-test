from pyparsing import Word, nums, alphas, Forward, Suppress, ZeroOrMore
import unittest

intStack = []
def pushStack(s, l, t):
    intStack.append(t[0])

atom = Word(nums).setParseAction(pushStack) | Suppress(Word(alphas))
expr = Forward()
expr << atom + ZeroOrMore(expr)

def evalString(string):
    return expr.parseString(string).asList()

class TestEx1(unittest.TestCase):

    def test_evalString(self):
        self.assertEqual(evalString("12ab34cd56ef"), ['12', '34', '56'])
        self.assertEqual(evalString("ab12cd34ef56"), ['12', '34', '56'])


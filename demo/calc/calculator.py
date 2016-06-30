from pyparsing import nums, Word, StringEnd, ParseException, Literal, ZeroOrMore, Forward
from calc.scalc import SimpleCalculator

"""
integer :: '0'...'9'*
addop   :: '+' | '-'
mulop   :: '*' | '/'
atom    :: integer | '(' + expr + ')'
term    :: atom [mulop atom]*
expr    :: term [addop term]*
"""

class Calculator:

    def __init__(self, calc = SimpleCalculator()):
        self.exprStack = []

        def pushStack(s, l, t):
            self.exprStack.append(t[0])

        integer = Word(nums).addParseAction(pushStack)
        addop = Literal('+') | Literal('-')
        mulop = Literal('*') | Literal('/')
        lpar = Literal('(')
        rpar = Literal(')')

        expr = Forward()
        atom = integer | lpar + expr + rpar
        term = atom + ZeroOrMore((mulop + atom).addParseAction(pushStack))
        expr << term + ZeroOrMore((addop + term).addParseAction(pushStack))
        self.expr = expr + StringEnd()

        self.opfun = {
                '+' : (lambda a, b: calc.add(a,b)),
                '-' : (lambda a, b: calc.sub(a,b)),
                '*' : (lambda a, b: calc.mul(a,b)),
                '/' : (lambda a, b: calc.div(a,b)) }

    def parseString(self, string):
        self.exprStack = []
        self.expr.parseString(string)
        return self.exprStack

    def evalStack(self, stack):
        op = stack.pop()
        if op in '+-*/':
            op2 = self.evalStack(stack)
            op1 = self.evalStack(stack)
            return self.opfun[op](op1, op2)
        else:
            return float(op)

    def evalString(self, string):
        try:
            self.parseString(string)
            return self.evalStack(self.exprStack)
        except ParseException:
            return 'Invalid Input'

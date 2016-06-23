# pyparsing 練習

這份文件不是 pyparsing 的完整說明，只為了把字串解析成數學運算式所做的練習與摸索。

以下透過一些練習，嘗試理解 [fourFn.py](http://pyparsing.wikispaces.com/file/view/fourFn.py) 這份解析工程數學運算式的程式碼。

## 練習一：熟悉 `Forward()`, `<<`, `setParseAction()`, `Suppress()`
ex1.py:
```python
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
```
- 解析字串，取出數字放入 `intStack`，忽略字母

```shell
$ python -m unittest -v ex1
test_evalString (ex1.TestEx1) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.002s

OK
```

## 練習二：簡單算數

ex2.py:
```python
from pyparsing import Word, Literal, nums, ZeroOrMore
import unittest

"""
op      :: '+' | '-' | '*' | '/'
num     :: '0'...'9'+
expr    :: num + [op + num]*
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

    def test_multiple_op(self):
        self.assertEqual(evalString('6+3+2'), 11.0)
        self.assertEqual(evalString('6-3-2'), 1.0)
        self.assertEqual(evalString('6*3*2'), 36.0)
        self.assertEqual(evalString('6/3/2'), 1.0)
```
- 解析數字與運算符號

```shell
$ python -m unittest -v ex2
test_evalStack (ex2.TestEx2) ... ok
test_evalString (ex2.TestEx2) ... ok
test_multiple_op (ex2.TestEx2) ... ok
test_parseString (ex2.TestEx2) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.005s

OK
```

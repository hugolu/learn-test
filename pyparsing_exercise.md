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

### step1 解析數字與運算符號，使用 unittest
ex2-1.py:
```python
from pyparsing import Word, Literal, nums, ParseResults
import unittest

"""
op      :: '+' | '-' | '*' | '/'
num     :: '0'...'9'+
expr    :: num + op + num
"""

add = Literal('+')
sub = Literal('-')
mul = Literal('*')
div = Literal('/')
op = add | sub | mul | div

num = Word(nums)

expr = num + op + num

def evalString(s):
    result = expr.parseString(s)
    return result.asList()

class MyTest(unittest.TestCase):

    def test_extract_symbol(self):
        self.assertEqual(evalString('3+2'), ['3', '+', '2'])
        self.assertEqual(evalString('3-2'), ['3', '-', '2'])
        self.assertEqual(evalString('3+2'), ['3', '+', '2'])
        self.assertEqual(evalString('3/2'), ['3', '/', '2'])
```
```shell
$ python -m unittest -v ex2-1
test_extract_symbol (ex2-1.MyTest) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```

### step2 加入 exprStack
```python
from pyparsing import Word, Literal, nums

"""
op      :: '+' | '-' | '*' | '/'
num     :: '0'...'9'+
expr    :: num + op + num
"""

add = Literal('+')
sub = Literal('-')
mul = Literal('*')
div = Literal('/')
op = add | sub | mul | div

exprStack = []
def pushStack(s, l, t):
    exprStack.append(t[0])

num = Word(nums).addParseAction(pushStack)

expr = num + (op + num).addParseAction(pushStack)

tests = ('3+2', '3-2', '3*2', '3/2')
for t in tests:
    exprStack = []
    expr.parseString(t)
    print(t, exprStack)
```
```
3+2 ['3', '2', '+']
3-2 ['3', '2', '-']
3*2 ['3', '2', '*']
3/2 ['3', '2', '/']
```

### step3 處理 exprStack
```python
from pyparsing import Word, Literal, nums

"""
op      :: '+' | '-' | '*' | '/'
num     :: '0'...'9'+
expr    :: num + op + num
"""

add = Literal('+')
sub = Literal('-')
mul = Literal('*')
div = Literal('/')
op = add | sub | mul | div

exprStack = []
def pushStack(s, l, t):
    exprStack.append(t[0])

def evalStack(stack):
    op = stack.pop()
    if op in '+-*/':
        op2 = evalStack(stack)
        op1 = evalStack(stack)
        if op == '+':
            return op1 + op2
        if op == '-':
            return op1 - op2
        if op == '*':
            return op1 * op2
        if op == '/':
            return op1 / op2
    else:
        return float(op)

num = Word(nums).addParseAction(pushStack)

expr = num + (op + num).addParseAction(pushStack)

tests = ('3+2', '3-2', '3*2', '3/2')
for t in tests:
    exprStack = []
    expr.parseString(t)
    print(t, exprStack, evalStack(exprStack[:]))
```
```
3+2 ['3', '2', '+'] 5.0
3-2 ['3', '2', '-'] 1.0
3*2 ['3', '2', '*'] 6.0
3/2 ['3', '2', '/'] 1.5
```

### step4 將 'op' 與對應的函式做成 dictionary
```python
from pyparsing import Word, Literal, nums

"""
op      :: '+' | '-' | '*' | '/'
num     :: '0'...'9'+
expr    :: num + op + num
"""

add = Literal('+')
sub = Literal('-')
mul = Literal('*')
div = Literal('/')
op = add | sub | mul | div

opf = { '+' : (lambda a, b: a+b),
        '-' : (lambda a, b: a-b),
        '*' : (lambda a, b: a*b),
        '/' : (lambda a, b: a/b) }

exprStack = []
def pushStack(s, l, t):
    exprStack.append(t[0])

def evalStack(stack):
    op = stack.pop()
    if op in '+-*/':
        op2 = evalStack(stack)
        op1 = evalStack(stack)
        return opf[op](op1, op2)
    else:
        return float(op)

num = Word(nums).addParseAction(pushStack)

expr = num + (op + num).addParseAction(pushStack)

tests = ('3+2', '3-2', '3*2', '3/2')
for t in tests:
    exprStack = []
    expr.parseString(t)
    print("%s = %d" % (t, evalStack(exprStack[:])))
```
```
3+2 = 5
3-2 = 1
3*2 = 6
3/2 = 1
```

### step5 加入 unittest
ex2-5.py:
```python
from pyparsing import Word, Literal, ZeroOrMore, nums
import unittest

"""
op      :: '+' | '-' | '*' | '/'
num     :: '0'...'9'+
expr    :: num + op + num
"""

add = Literal('+')
sub = Literal('-')
mul = Literal('*')
div = Literal('/')
op = add | sub | mul | div

exprStack = []
def pushStack(s, l, t):
    exprStack.append(t[0])

num = Word(nums).addParseAction(pushStack)

expr = num + ZeroOrMore((op + num).addParseAction(pushStack))

opf = { '+' : (lambda a, b: a+b),
        '-' : (lambda a, b: a-b),
        '*' : (lambda a, b: a*b),
        '/' : (lambda a, b: a/b) }

def evalStack(stack):
    op = stack.pop()
    if op in '+-*/':
        op2 = evalStack(stack)
        op1 = evalStack(stack)
        return opf[op](op1, op2)
    else:
        return float(op)

def evalString(string):
    global exprStack, expr
    exprStack = []
    expr.parseString(string)
    return evalStack(exprStack)

class MyTest(unittest.TestCase):

    def test_simple_op(self):
        self.assertEqual(evalString('6+3'), 9.0)
        self.assertEqual(evalString('6-3'), 3.0)
        self.assertEqual(evalString('6*3'), 18.0)
        self.assertEqual(evalString('6/3'), 2.0)

    def test_multi_op(self):
        self.assertEqual(evalString('6+3+2'), 11.0)
        self.assertEqual(evalString('6-3-2'), 1.0)
        self.assertEqual(evalString('6*3*2'), 36.0)
        self.assertEqual(evalString('6/3/2'), 1.0)
```
```shell
$ python -m unittest -v ex2-5
test_multi_op (ex2-5.MyTest) ... ok
test_simple_op (ex2-5.MyTest) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.003s

OK
```

# pyparsing 練習

這份文件不是 pyparsing 的完整說明，只為了把字串解析成數學運算式所做的練習與摸索。

以下透過一些練習，嘗試理解 [fourFn.py](http://pyparsing.wikispaces.com/file/view/fourFn.py) 這份解析工程數學運算式的程式碼。

## 練習一：熟悉 `Forward()`, `<<`, `setParseAction()`, `Suppress()`

完整程式碼: [ex1.py](pyparsing/ex1.py)
```python
intStack = []
def pushStack(s, l, t):
    intStack.append(t[0])

atom = Word(nums).setParseAction(pushStack) | Suppress(Word(alphas))
expr = Forward()
expr << atom + ZeroOrMore(expr)
```
- 解析字串，取出數字放入 `intStack`，忽略字母

## 練習二：簡單算數: 解析數字與運算符號

完整程式碼: [ex2.py](pyparsing/ex2.py)
```python
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
```
- 滿足簡單加減乘除運算，但運算符號沒有次序性，所以只能解析如: '1+2+3-4', '1*2*3/4'，無法處理加減乘除混合運算

```python
def parseString(string):
    global exprStack
    exprStack = []
    expr.parseString(string)
    return exprStack
```
- 將字串轉成運算的 stack，如 '1+2' => ['1', '2', '+']

```python
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
```
- 處理 exprStack，取出元素如果是
    - 運算元(numbers)，轉成浮點數 (可能當作除法除數或被除數)，回傳結果
    - 運算子(+,-,*,/) 後再取出兩個運算元，呼叫運算子函數，傳入剛剛得到的運算元，回傳運算結果

```python
def evalString(string):
    stack = parseString(string)
    result = evalStack(stack)
    return result
```
- 結合 `parseString()` 與 `evalStack()`，求出輸入字串的運算結果

## 練習三：符合先乘除、後加減

完整程式碼: [ex3.py](pyparsing/ex3.py)
```python
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
```
- `expr` 先處理 `term`，再處理加減運算
- `term` 先處理 `atom`，再處理乘除運算

## 練習四：括號優先權大於加減乘除

完整程式碼: [ex4.py](pyparsing/ex4.py)
```python
"""
op      :: '+' | '-' | '*' | '/'
integer :: '0'...'9'+
atom    :: integer | '(' expr ')'
term    :: atom [mulop atom]*
expr    :: term [addop term]*
"""

exprStack = []
def pushFirst(s, l, t):
    exprStack.append(t[0])

add = Literal('+')
sub = Literal('-')
mul = Literal('*')
div = Literal('/')
lpar = Literal('(')
rpar = Literal(')')
addop = add | sub
mulop = mul | div

expr = Forward()
atom = Word(nums).addParseAction(pushFirst) | (lpar + expr + rpar)
term = atom + ZeroOrMore((mulop + atom).addParseAction(pushFirst))
expr << term + ZeroOrMore((addop + term).addParseAction(pushFirst))
```
- 最基本的運算單位可能是"整數"或是"有括號的運算式"
    - 如果是整數，處理後推入 exprStack
    - 如果是括號運算式，進行遞迴求出括號裡面的值

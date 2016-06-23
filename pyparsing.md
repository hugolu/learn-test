# pyparsing

這份文件不是 pyparsing 的完整說明，只為了把字串解析成數學運算式所做的練習與摸索。

除了 [Getting Started with Pyparsing](http://shop.oreilly.com/product/9780596514235.do) 這本書，pyparsing 似乎沒有完整的說明文件？！

以下透過一些練習，嘗試理解 [fourFn.py](http://pyparsing.wikispaces.com/file/view/fourFn.py) 這份解析工程數學運算式的程式碼。

## pyparsing: 從本文抽取訊息的工具

pyparsing 模組提供程式設計師使用 python 語言從結構化的文本資料抽取資訊。

這個工具比正規化表示式更強大 (python re 模組)，但又不像編譯器那樣一般化。

為了找出結構化文本中的訊息，我們必須描述結構。pyparsing 模組建立在 [Backus-Naur Form](https://en.wikipedia.org/wiki/Backus%E2%80%93Naur_Form) (BNF) 語法描述技術的基礎上。熟悉 BNF 的語法標記有助於使用 pyparsing。

pyparsing 模組運作的方式是使用遞迴減少解析器 [recursive descent parser](https://en.wikipedia.org/wiki/Recursive_descent_parser) 匹配輸入文字：我們寫出像 BNF 語法產物，然後 pyparsing 提供機制用這些產物匹配輸入文本。

The pyparsing module works best when you can describe the exact syntactic structure of the text you are analyzing. A common application of pyparsing is the analysis of log files. Log file entries generally have a predictable structure including such fields as dates, IP addresses, and such. Possible applications of the module to natural language work are not addressed here.

當你能精準描述分析的文本結構，pyparsing 模組就能發揮強大的作用。通常 pyparsing 會拿來分析 log 檔。log 檔通常有個可預測的結構，欄位包含日期、IP位置、等等。

## 建構應用程式

1. 寫出 BNF 描述要分析文本的結構
2. 視需要，安裝 pyparsing 模組
3. 在 python script 中匯入 pyparsing 模組：`import pyparsing as pp`
4. 在 python script 中寫出能匹配 BNF 的 parser
5. 準備要分析的文本
6. 如果用 p 表示 parser，用 s 表示文本，執行的程式碼就像 `p.parseString(s)`
7. 從解析結果得到需要的訊息

## 一個小型完整的範例

python 識別符號包含一個或多的字元，第一個字元是 字母或 `_`，接著可能是 字母、數字、或 `_`。用 BNF 方式寫成

```
first       ::=  letter | "_"
letter      ::=  "a" | "b" | ... "z" | "A" | "B" | ... | "Z"
digit       ::=  "0" | "1" | ... | "9"
rest        ::=  first | digit
identifier  ::=  first rest*
```

最終產出物可讀作：一個識別符號包含一個 `first`，接著可能有零個或多個 `rest`。

以下程式碼
```python
#!/usr/bin/env python
#================================================================
# trivex: Trivial example
#----------------------------------------------------------------

# - - - - -   I m p o r t s

import sys

import pyparsing as pp

# - - - - -   M a n i f e s t   c o n s t a n t s

first = pp.Word(pp.alphas+"_", exact=1)
rest = pp.Word(pp.alphanums+"_")
identifier = first+pp.Optional(rest)

testList = [ # List of test strings    
    # Valid identifiers
    "a", "foo", "_", "Z04", "_bride_of_mothra",
    # Not valid
    "", "1", "$*", "a_#" ]

# - - - - -   m a i n

def main():
    """
    """
    for text in testList:
        test(text)

# - - -   t e s t

def test(s):
    '''See if s matches identifier.
    '''
    print ("---Test for '{0}'".format(s))

    try:
        result = identifier.parseString(s)
        print "  Matches: {0}".format(result)
    except pp.ParseException as x:
        print "  No match: {0}".format(str(x))

# - - - - -   E p i l o g u e

if __name__ == "__main__":
    main()
```
```
$ python trivex.py
---Test for 'a'
  Matches: ['a']
---Test for 'foo'
  Matches: ['f', 'oo']
---Test for '_'
  Matches: ['_']
---Test for 'Z04'
  Matches: ['Z', '04']
---Test for '_bride_of_mothra'
  Matches: ['_', 'bride_of_mothra']
---Test for ''
  No match: Expected W:(ABCD...) (at char 0), (line:1, col:1)
---Test for '1'
  No match: Expected W:(ABCD...) (at char 0), (line:1, col:1)
---Test for '$*'
  No match: Expected W:(ABCD...) (at char 0), (line:1, col:1)
---Test for 'a_#'
  Matches: ['a', '_']
```

回傳值是 `pp.ParseResults class` 的實例。當列印出來，會像個 list。單一字母的測試字串只有一個元素，多字母字串有兩個元素，一個是 `first` 接著是 `rest`。

如果想讓回傳值合併匹配的元素，使用 
```python
identifier = pp.Combine(first+pp.Optional(rest))
```

結果會像這樣
```
---Test for '_bride_of_mothra'
  Matches: ['_bride_of_mothra']
```

## 如何組織回傳結果 ParseResults

當輸入與建立的解析器匹配，`.parseString()` 回傳 `class ParseResults` 的實例。

對於一個複雜的結構，這個實例可能有很多訊息在裡面。`ParseResults` 實例的結構跟你如何建立解析器有關。

存取 `ParserResults` 有幾種方式：
- 當作一個 list
```python
>>> import pyparsing as pp
>>> number = pp.Word(pp.nums)
>>> result = number.parseString('17')
>>> print result
['17']
>>> type(result)
<class 'pyparsing.ParseResults'>
>>> result[0]
'17'
>>> list(result)
['17']
>>> numberList = pp.OneOrMore(number)
>>> print numberList.parseString('17 33 88')
['17', '33', '88']
```
- 當作一個 dictionary
```python
>>> number = pp.Word(pp.nums).setResultsName('nVache')
>>> result = number.parseString('17')
>>> print result
['17']
>>> result['nVache']
'17'
```

### 使用 `pp.Group()` 分而治之

如果採取分而治之的原則 (分段精練)，解析器的組織會更容易追蹤理解。

實例上，這個意指頂層的 `ParseResults` 應該包含更多子部分。
如果這一層有太多子部分，查看輸入把它拆解成兩個或更多的子解析器。
然後組織頂層，它只會包含這些。
如果需要，拆解小解析器成為更小的，直到每個解析器都能用內建的基礎功能清楚定義。

----
## `Word`: Match characters from a specified set

```python
from pyparsing import Word
from pyparsing import nums, alphas, alphanums

name = Word('abcdef')
print(name.parseString('fadedglory'))

pyName = Word(alphas + '_', bodyChars = alphanums + '_')
print(pyName.parseString('_crunchyFrog13'))

name4 = Word(alphas, exact=4)
print(name4.parseString('Whizzo'))

noXY = Word(alphas, excludeChars='xy')
print(noXY.parseString('Sussex'))
```
```
['faded']
['_crunchyFrog13']
['Whiz']
['Susse']
```
## `ZeroOrMore`: Match any number of repetitions including none

```python
from pyparsing import Word, ZeroOrMore
from pyparsing import nums, alphas

item = Word(nums) | Word(alphas)
expr = ZeroOrMore(item)
bnf = expr

tests = ("123abc456def", "123 abc 456 def", "abc def 123 456")

for t in tests:
    print(t, " >>> ", bnf.parseString(t))
```
```
123abc456def  >>>  ['123', 'abc', '456', 'def']
123 abc 456 def  >>>  ['123', 'abc', '456', 'def']
abc def 123 456  >>>  ['abc', 'def', '123', '456']
```

## `Suppress`: Omit matched text from the result
```python
from pyparsing import Word, Literal, Suppress
from pyparsing import nums, alphas, alphanums

name = Word(alphas)
lb = Literal('[')
rb = Literal(']')

pat1 = lb + name + rb
print(pat1.parseString('[Pewty]'))

pat2 = Suppress(lb) + name + Suppress(rb)
print(pat2.parseString('[Pewty]'))
```
```
['[', 'Pewty', ']']
['Pewty']
```

## `CharsNotIn`: Match characters not in a given set

```python
from pyparsing import CharsNotIn
from pyparsing import nums

nonDigits = CharsNotIn(nums)
print(nonDigits.parseString('zoot86'))

fourNonDigits = CharsNotIn(nums, exact=4)
print(fourNonDigits.parseString('a$_/#'))
```
```
['zoot']
['a$_/']
```

## `CaselessLiteral`: Case-insensitive string match

```python
from pyparsing import CaselessLiteral

ni = CaselessLiteral('Ni')

print(ni.parseString('Ni'))
print(ni.parseString('NI'))
print(ni.parseString('nI'))
print(ni.parseString('ni'))
```
```
['Ni']
['Ni']
['Ni']
['Ni']
```

## `Forward()`

Forward declaration of an expression to be defined later - used for recursive grammars, such as algebraic infix notation. When the expression is known, it is assigned to the Forward variable using the '<<' operator.

```python
#!/usr/bin/env python
#================================================================
# hollerith:  Demonstrate Forward class
#----------------------------------------------------------------
import sys
from pyparsing import Word, Forward, Suppress, CaselessLiteral
from pyparsing import ParseException, CharsNotIn
from pyparsing import nums

# - - - - -   M a n i f e s t   c o n s t a n t s

TEST_STRINGS = [ '1HX', '2h$#', '10H0123456789', '999Hoops']

# - - - - -   m a i n

def main():
    holler = hollerith()
    for text in TEST_STRINGS:
        test(holler, text)

# - - -   t e s t

def test(pat, text):
    '''Test to see if text matches parser (pat).
    '''
    print ("--- Test for '{0}'".format(text))
    try:
        result = pat.parseString(text)
        print ("  Matches: '{0}'".format(result[0]))
    except ParseException as x:
        print ("  No match: '{0}'".format(str(x)))

# - - -   h o l l e r i t h

def hollerith():
    '''Returns a parser for a FORTRAN Hollerith character constant.
    '''

    #--
    # Define a recognizer for the character count.
    #--
    intExpr = Word(nums).setParseAction(lambda t: int(t[0]))
    
    #--
    # Allocate a placeholder for the rest of the parsing logic.
    #--
    stringExpr = Forward()

    #--
    # Define a closure that transfers the character count from
    # the intExpr to the stringExpr.
    #--
    def countedParseAction(toks):
        '''Closure to define the content of stringExpr.
        '''
        n = toks[0]

        #--
        # Create a parser for any (n) characters.
        #--
        contents = CharsNotIn('', exact=n)

        #--
        # Store a recognizer for 'H' + contents into stringExpr.
        #--
        stringExpr << (Suppress(CaselessLiteral('H')) + contents)

        return None
    #--
    # Add the above closure as a parse action for intExpr.
    #--
    intExpr.addParseAction(countedParseAction)

    #--
    # Return the completed pattern.
    #--
    return (Suppress(intExpr) + stringExpr)

# - - - - -   E p i l o g u e

if __name__ == "__main__":
    main()
```

`hollerith()` 怎麼運作的，故事倒著說
- `(Suppress(intExpr) + stringExpr)` 先對字串執行 `intExptr`，處理過的字串忽略結果，然後執行 `stringExpr`
    - `stringExptr` 是個 `Forward()` 生出來的 placeholder
    - `intExpr = Word(nums).setParseAction(lambda t: int(t[0]))`，匹配字串成數字，將數字解析成 `int`
        - `intExpr.addParseAction(countedParseAction)` 剛剛解析處來的 `int` 傳入 `countedParseAction()`
        - `countedParseAction()` 組合 `(Suppress(CaselessLiteral('H')) + contents)` 存到 `stringExpr`
            - `Suppress(CaselessLiteral('H'))` 匹配不分大小寫字母 `H`，但忽略結果
            - `contents = CharsNotIn('', exact=n)` 匹配n個任意字元

輸入 `10H0123456789`：
- `10` 會被 `intExpr` 解釋成整數 10 (忽略結果)
- `H` 會被 `Suppress(CaselessLiteral('H'))` 匹配到 (忽略結果)
- `0123456789` 會被 `contents` 匹配到，取出字串

```
--- Test for '1HX'
  Matches: 'X'
--- Test for '2h$#'
  Matches: '$#'
--- Test for '10H0123456789'
  Matches: '0123456789'
--- Test for '999Hoops'
  No match: 'Expected !W:() (at char 8), (line:1, col:9)'
```
----
## 練習一：熟悉 `Forward()`, `<<`, `setParseAction()`, `Suppress()`
```python
from pyparsing import Word, nums, alphas, Forward, Suppress, ZeroOrMore

intStack = []
def pushStack(s, l, t):
    intStack.append(t[0])

atom = Word(nums).setParseAction(pushStack) | Suppress(Word(alphas))
expr = Forward()
expr << atom + ZeroOrMore(expr)

expr.parseString("12ab34cd56ef78gh90ij")
print(intStack)
```
- 解析字串 "123abc456def789ghi0"，取出數字放入 `intStack`，忽略字母
```
['12', '34', '56', '78', '90']
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
----
## 參考

- [Pyparsing Wiki Home](http://pyparsing.wikispaces.com/)
- [pyparsing quick reference](http://infohost.nmt.edu/tcc/help/pubs/pyparsing/web/index.html) - 說明＆範例
- [Module pyparsing](https://pythonhosted.org/pyparsing/)

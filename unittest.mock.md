# unittest.mock

unittest.mock 是 python 用於測試的函式庫，用 mock 物件替換待測試系統的某些部分，宣告這些偽造的部分應該如何被使用。

## Test Double

[介紹Test Double](http://teddy-chen-tw.blogspot.tw/2014/09/test-double1.html)之前先介紹兩個測試常用術語：

- SUT：System Under Test或Software Under Test的簡寫，代表待測程式。如果是單元測試，SUT就是一個function或method。
- DOC：Depended-on Component（相依元件），又稱為Collaborator（合作者）。DOC是SUT執行的時候會使用到的元件。例如，有一個函數X如果執行失敗會寄送email，則email元件就是函數X的DOC。

[Test Double 的種類](http://www.martinfowler.com/bliki/TestDouble.html):
- **Dummy** 用來傳遞給函式但不會真的被使用，通常只充當函式參數讓程式順利編譯。
- **Fake** 物件真正功能，但通常會採用捷徑實作，不適合用在生產環境。(範例：InMemoryTestDatabase)
- **Stub** 為測試時期的呼叫提供罐裝答案，通常不會對外界所有輸入做出反應。
- **Spy** 記錄他們怎麼被呼叫的資訊。
- **Mock** 是一連串預先編排的執行動作，對特定預期的呼叫做出反應，如果收到非預期呼叫方式則丟出例外。



## 快速導覽

### 範例一
Something.py:
```python
class Something:
    def method(self, a, b, c, key):
        print(a, b, c, key)
        return 3
```

testSomething.py
```python
import unittest
from unittest.mock import MagicMock
from Something import Something

class TestSomethingCases(unittest.TestCase):

    def test_return_value(self):
        s = Something()
        self.assertEqual(s.method(1,2,3,key='hello'), 3)

    def test_mock_return_value(self):
        something = Something()
        something.method = MagicMock(return_value = 5)
        self.assertEqual(something.method(1, 2, 3, key='hello'), 5)

    def test_mock_called_with(self):
        something = Something()
        something.method = MagicMock(return_value = 5)
        something.method(3,4,5,key='value')
        something.method.assert_called_with(3, 4, 5, key='value')
```
- `test_return_value` 檢查物件方法預設回傳值
- `test_mock_return_value` 偽造方法回傳值 (Stub)
- `test_mock_called_with` 檢查方法呼叫是否如預期 (Spy or Mock)

testing:
```shell
$ python -m unittest -v testSomething
test_mock_called_with (testSomething.TestSomethingCases) ... ok
test_mock_return_value (testSomething.TestSomethingCases) ... ok
test_return_value (testSomething.TestSomethingCases) ... 1 2 3 hello
ok

----------------------------------------------------------------------
Ran 3 tests in 0.004s

OK
```

### 範例二

`side_effect` 允許執行副作用，包含當 mock 被呼叫時產生例外。

```python
>>> from unittest.mock import Mock
>>> mock = Mock(side_effect=KeyError('foo'))
>>> mock()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3.4/unittest/mock.py", line 902, in __call__
    return _mock_self._mock_call(*args, **kwargs)
  File "/usr/lib/python3.4/unittest/mock.py", line 958, in _mock_call
    raise effect
KeyError: 'foo'
```
- 呼叫 `mock` 產生例外

```python
>>> values ={'a' : 1, 'b' : 2, 'c' : 3}
>>> def side_effect(arg):
...     return values[arg]
...
>>> mock.side_effect = side_effect
>>> mock('a'), mock('b'), mock('c')
(1, 2, 3)
```
- 透過 `side_effect()` 控制呼叫 `mock` 時回應的值

```python
>>> mock.side_effect = [5, 4, 3, 2, 1]
>>> mock(), mock(), mock()
(5, 4, 3)
```
- 預設呼叫 `mock` 回應的值

### 範例三

----

## Using Mock

### Mock Patching Methods

Mock 通常用在

- 取代物件方法 (stub)
- 檢查物件方法呼叫是否合乎預期 (spy)

```python
>>> from unittest.mock import MagicMock
>>> class SomeClass:
...     def method(self, a, b, c):
...             return a + b + c
...
>>> real = SomeClass()
>>> real.method(1,2,3)
6
>>> real.method = MagicMock(name='method')
>>> real.method(2,3,4)
<MagicMock name='method()' id='139869459937992'>
>>> real.method.assert_called_with(2,3,4)
```
### Mock for Method Calls on an Object

傳遞物件給方法，檢查物件是否被正確使用

```python
>>> class ProductionClass:
...     def closer(self, something):
...             something.close()
...
>>> real = ProductionClass()
>>> mock = MagicMock()
>>> real.closer(mock)
>>> mock.close.assert_called_with()
```
- `ProductionClass.closer` 會呼叫傳入參數的方法 `something.close()`
- `mock = MagicMock()` 產生 spy 傳入方法中，然後檢是否被正確呼叫

### Mocking Classes

常見的情況是要在測試中用替換某類別，當你 patch 一個類別，這個類別就被 mock 取代。類別的物件是在被呼叫的方法中產生，你可以藉由查看被偽裝類別的回傳值存取偽裝物件。

> 不用 IoC 嗎？

module.py:
```python
class Foo:
    def method(self):
        return 'foo'
```

software under test:
```python
>>> import module
>>> def some_function():
...     instance = module.Foo()
...     return instance.method()
...
>>> some_function()
'foo'
```

用 mock 取代 `module.Foo`
```python
>>> from unittest.mock import patch
>>> with patch('module.Foo') as mock:
...     instance = mock.return_value
...     instance.method.return_value = 'bar
...     result = some_function()
...     assert result == 'bar'
```

### Naming your mocks

命名 mock 物件，當出現錯誤可以快速找到原因

```python
>>> from unittest.mock import MagicMock
>>> mock = MagicMock(name='foo')
>>> mock
<MagicMock name='foo' id='140366347445360'>
>>> mock.method
<MagicMock name='foo.method' id='140366338380744'>
```

### Tracking all Calls

`mock_calls` 屬性紀錄所有呼叫 mock 與其子類的歷程

```python
>>> from unittest.mock import MagicMock
>>> mock = MagicMock()
>>> mock.method(1)
<MagicMock name='mock.method()' id='140667031061560'>
>>> mock.method(2)
<MagicMock name='mock.method()' id='140667031061560'>
>>> mock.method(3)
<MagicMock name='mock.method()' id='140667031061560'>
>>> mock.mock_calls
[call.method(1), call.method(2), call.method(3)]
```
### Setting Return Values and Attributes

設定 mock 回傳值很簡單
```python
>>> from unittest.mock import Mock
>>> mock = Mock()
>>> mock.return_value = 3
>>> mock()
```

可以定義 mock 方法的回傳值
```python
>>> mock = Mock()
>>> mock.method.return_value = 3
>>> mock.method()
3
```

可以在建構函式中宣告回傳值
```python
>>> mock = Mock(return_value = 3)
>>> mock()
3
```

可以設定 mock 的屬性值
```python
>>> mock = Mock()
>>> mock.x = 3
>>> mock.x
3
```

有時候要設定更複雜的情況，例如 `mock.connection.cursor().execute("SELECT 1")`，如果希望回傳一個陣列，就要設定一個遞迴呼叫的回傳結果。
```python
>>> from unittest.mock import call
>>> mock = Mock()
>>> cursor = mock.connection.coursor.return_value
>>> cursor.execute.return_value = ['foo']
>>> mock.connection.coursor().execute("SELECT 1")
['foo']
>>> expected = call.connection.coursor().execute("SELECT 1").call_list()
>>> mock.mock_calls
[call.connection.coursor(), call.connection.coursor().execute('SELECT 1')]
>>> mock.mock_calls == expected
True
```
- `cursor = mock.connection.coursor.return_value` 產生第一個回傳值，回傳一個 `cursor`
- `cursor.execute.return_value = ['foo']` 設定執行第一個回傳值的結果，回傳一個陣列

使用偽造的 cursor 查詢資料庫
```python
>>> cursor.execute("SELECT 1")
['foo']
```

### Raising exceptions with mocks

做出一個會產生例外的 mock
```python
>>> from unittest.mock import Mock
>>> mock = Mock(side_effect=Exception('Boom!'))
>>> mock()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3.4/unittest/mock.py", line 902, in __call__
    return _mock_self._mock_call(*args, **kwargs)
  File "/usr/lib/python3.4/unittest/mock.py", line 958, in _mock_call
    raise effect
Exception: Boom!
```

### Side effect functions and iterables

`side_effect` 可以設定為函數或 **iterable**。當 mock 預計要被多次呼叫，每次回傳不同的值。當設定 side_effect 成為 iterable，每次呼叫會從 iterable 回傳 next value。

```python
>>> from unittest.mock import MagicMock
>>> mock = MagicMock(side_effect=[4,5,6])
>>> mock()
4
>>> mock()
5
>>> mock()
6
>>> mock()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3.4/unittest/mock.py", line 902, in __call__
    return _mock_self._mock_call(*args, **kwargs)
  File "/usr/lib/python3.4/unittest/mock.py", line 961, in _mock_call
    result = next(effect)
StopIteration
```

更進階用法是根據傳入參數變化回傳的值，此時 side_effect 可以是個 **function**。下例透過 dictionary 偽造傳入參數與回傳值的對應關係。
```python
>>> vals = {(1,2): 1, (2,3): 2}
>>> def side_effect(*args):
...     return vals[args]
...
>>> mock = MagicMock(side_effect=side_effect)
>>> mock(1,2)
1
>>> mock(2,3)
2
```

### Creating a Mock from an Existing Object

有時隨著時間演進，測試與待測物變得不匹配，例如 `Foo` 原先有 `old_method` 方法，但後來改成 `method`。使用 spec 關鍵字，當存取的方法或屬性不存在於 spec 定義的物件中，就會立即產生錯誤。

```python
>>> class Foo:
...     def method():
...             return 'foo'
...
>>> mock = Mock(spec=Foo)
>>> mock.method.return_value = 'bar'
>>> mock.method()
'bar'
>>> mock.old_method.return_value = 'baz'
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/usr/lib/python3.4/unittest/mock.py", line 574, in __getattr__
    raise AttributeError("Mock object has no attribute %r" % name)
AttributeError: Mock object has no attribute 'old_method'
```

也可以使用 spec 定義呼叫 mock 的方法，不管參數是根據位置傳遞或是依照參數名稱傳遞。
```python
>>> def f(a,b,c): pass
...
>>> mock = Mock(spec=f)
>>> mock(1,2,3)
<Mock name='mock()' id='140452137637368'>
>>> mock.assert_called_with(a=1, b=2, c=3)
>>> mock(c=3, b=2, a=1)
<Mock name='mock()' id='140452137637368'>
>>> mock.assert_called_with(a=1, b=2, c=3)
```

## Patch Decorators

“使用patch或者patch.object的目的是为了控制mock的范围，意思就是在一个函数范围内，或者一个类的范围内，或者with语句的范围内mock掉一个对象。” - [Python Mock的入门](https://segmentfault.com/a/1190000002965620)

- [`patch()`](https://docs.python.org/3.4/library/unittest.mock.html#unittest.mock.patch) acts as a function decorator, class decorator or a context manager. Inside the body of the function or with statement, the target is patched with a new object. When the function/with statement exits the patch is undone.
- [`patch.object()`](https://docs.python.org/3.4/library/unittest.mock.html#unittest.mock.patch.object) can be used as a decorator, class decorator or a context manager. Arguments new, spec, create, spec_set, autospec and new_callable have the same meaning as for patch(). Like patch(), patch.object() takes arbitrary keyword arguments for configuring the mock object it creates.

Game.py:
```python
import random

def choice(*seq):
    return random.choice(seq)

class Game:
    def coin(self):
        return choice(['head', 'tail'])

    def bet(self, side):
        return 'win' if side == self.coin() else 'lose'
```
- `choice()` 隨機回傳 seq 裡面任意元素
- `coin()` 透過 `choice()` 決定硬幣正反面
- `bet()` 判斷 `side` 與 `coin()` 是否相同，決定輸贏

testGame.py:
```python
import unittest
from unittest.mock import patch

class TestGame(unittest.TestCase):

    def test_head_tail(self):
        def always_tail(self):
            return 'tail'
        with patch('Game.choice', always_tail):
            from Game import Game
            game = Game()
            self.assertEqual(game.bet('head'), 'lose')

    def test_head_head(self):
        from Game import Game
        def always_head(self):
            return 'head'
        with patch.object(Game, 'coin', always_head):
            game = Game()
            self.assertEqual(game.bet('head'), 'win')
```

為了測試 `Game.bet` 裡面判斷輸贏的邏輯是否正確，必須將底層的依賴元件取代為可操作結果的 test double。取代有兩種方式，`patch` 與 `patch.object`：

- `test_head_tail`: 用 `always_tail` 取代 `Game` 模組的 `choice` 函式
- `test_head_head`: 用 `always_head` 取代 `Game` 類別的 `coni` 方法

run test:
```chell
$ python -m unittest -v test
test_head_head (test.TestGame) ... ok
test_head_tail (test.TestGame) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.010s

OK
```

## Further Examples

### Mocking chained calls

一旦理解 `return_value` 這個屬性，偽裝一連串的呼叫使用上會很直覺。當 `mock` 第一次被呼叫，或是在呼叫前讀取 `return_value`，新的 `mock` 物件就因應而生。

```python
>>> from unittest.mock import Mock
>>> mock = Mock()
>>> mock().foo(a=2,b=3)
<Mock name='mock().foo()' id='139808365932616'>
>>> mock.return_value.foo.assert_called_with(a=2,b=3)
```
- 呼叫 `mock()` 則產生一個新的 mock 物件，然後繼續呼叫新 mock 物件的方法 `foo(a=2,b=3)` 
- 最後用 `mock.return_value.foo.assert_called_with(a=2,b=3)` 檢查一開始的 `mock` 產生的物件 `mock.return_value` 的 `foo` 方法是否以 `(a=2,b=3)` 方式呼叫

### Partial mocking
### Mocking a Generator Method
### Applying the same patch to every test method
### Mocking Unbound Methods
### Checking multiple calls with mock
### Coping with mutable arguments
### Nesting Patches
### Mocking a dictionary with MagicMock
### Mock subclasses and their attributes
### Mocking imports with patch.dict
### Tracking order of calls and less verbose call assertions
### More complex argument matching

----
## 參考
- [unittest.mock — mock object library
](https://docs.python.org/3.4/library/unittest.mock.html)
- [unittest.mock — getting started](https://docs.python.org/3.4/library/unittest.mock-examples.html)

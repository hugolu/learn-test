# unittest.mock

參考 - [unittest.mock — mock object library
](https://docs.python.org/3.4/library/unittest.mock.html), [unittest.mock — getting started](https://docs.python.org/3.4/library/unittest.mock-examples.html)

unittest.mock 是 python 用於測試的函式庫，用 mock 物件替換待測試系統的某些部分，宣告這些偽造的部分應該如何被使用。

## Test Double
參考 - [TestDouble](http://www.martinfowler.com/bliki/TestDouble.html)

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
### Naming your mocks
### Tracking all Calls
### Setting Return Values and Attributes
### Raising exceptions with mocks
### Side effect functions and iterables
### Creating a Mock from an Existing Object

## Patch Decorators

## Further Examples
### Mocking chained calls
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

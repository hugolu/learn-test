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

# unittest 筆記

參考：[unittest — Unit testing framework](https://docs.python.org/3/library/unittest.html)

Python unittest 測試框架發想自 JUnit 並與其他單元測試的框架有類似的味道：

- 支援自動化測試
- 測試間共享 setup 與 shutdown 程式碼
- 每次測試皆是獨立，結果不會受其他測試影響

| 名詞 | 解釋 |
|------|------|
| 測試夾具 (test fixture) | 包含一個或多個被執行的測試，與相關的初始與結束動作。 |
| 測試案例 (test case) | 個別單元測試，用來檢查特定輸入的反應。 |
| 測試套組 (test suite) | 由測試案例、測試套組構成，用來集合應該被一起執行的測試。 |
| 測試執行 (test runner) | 負責執行測試與回報結果。 |

## 基本範例

Arithmetic.py:
```python
import unittest

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

class TestArithmetic(unittest.TestCase):

    def test_add(self):
        self.assertEqual(add(1, 1), 2)

    def test_subtract(self):
        self.assertEqual(subtract(5, 2), 3)

    def test_multiply(self):
        self.assertEqual(multiply(3, 2), 6)

    def test_divide(self):
        self.assertEqual(divide(3.0, 2), 1.5)

if __name__ == '__main__':
    unittest.main()
```

- `test_add` 測試 `add()` 函數是否正確運作
- `test_subtract` 測試 `subtract()` 函數是否正確運作
- `test_multiply` 測試 `multiply()` 函數是否正確運作
- `test_divide` 測試 `divide()` 函數是否正確運作
- `if __name__ == '__main__'` 判斷是否執行執行，若是則執行測試

執行結果：
```shell
$ python Arithmetic.py
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
/tmp/test$ python Arithmetic.py -v                      # 使用參數 -v 提供測試細節
test_add (__main__.TestArithmetic) ... ok
test_divide (__main__.TestArithmetic) ... ok
test_multiply (__main__.TestArithmetic) ... ok
test_subtract (__main__.TestArithmetic) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
```

## 命令列

TestArithmetic.py:
```python
import unittest

class TestArithmetic(unittest.TestCase):

    def test_add(self):
        self.assertEqual(1 + 1, 2)

    def test_subtrat(self):
        self.assertEqual(5 - 2, 3)

    def test_multiply(self):
        self.assertEqual(2 * 3, 6)

    def test_divide(self):
        self.assertEqual(3.0 / 2, 1.5)
```

執行結果：
```shell
$ python -m unittest -h                                 # 顯示 help message
$ python -m unittest TestArithmetic                     # 測試 TestArithmetic 模組，不含副檔名 (.py)
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
$ python -m unittest TestArithmetic.TestArithmetic      # 測試 TestArithmetic 模組的 TestArithmetic 類別
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
$ python -m unittest TestArithmetic.TestArithmetic.test_add # 測試 TestArithmetic 模組的 TestArithmetic 類別的 test_add 測試項目
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
$ python -m unittest -v TestArithmetic                  # 顯示測試細節
test_add (TestArithmetic.TestArithmetic) ... ok
test_divide (TestArithmetic.TestArithmetic) ... ok
test_multiply (TestArithmetic.TestArithmetic) ... ok
test_subtrat (TestArithmetic.TestArithmetic) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.000s

OK
$ python -m unittest TestArithmetic TestStringMethods   # 測試兩個模組
.......
----------------------------------------------------------------------
Ran 7 tests in 0.000s

OK
```

## 測試探索

```shell
$ ls
TestArithmetic.py    TestStringMethods.py
$ python -m unittest discover -p "Test*.py"             # 找出 "Test*.py" 的檔案測試
.......
----------------------------------------------------------------------
Ran 7 tests in 0.000s

OK
$ python -m unittest discover -v -p "Test*.py"          # 找出 "Test*.py" 的檔案測試，並顯示測試細節
test_add (TestArithmetic.TestArithmetic) ... ok
test_divide (TestArithmetic.TestArithmetic) ... ok
test_multiply (TestArithmetic.TestArithmetic) ... ok
test_subtrat (TestArithmetic.TestArithmetic) ... ok
test_isupper (TestStringMethods.TestStringMethods) ... ok
test_split (TestStringMethods.TestStringMethods) ... ok
test_upper (TestStringMethods.TestStringMethods) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.000s

OK
```

> 不清楚文件提到的 test suite 怎麼弄，先 pass

## 重新使用舊測試

(略)

## 忽略測試與預期的錯誤

testSkip.py:
```python
import unittest
import sys

__version__ = (1, 2)

class TestSkipCase(unittest.TestCase):

    @unittest.skip("demonstrating skipping")
    def test_nothing(self):
        self.fail("shouldn't happen")

    @unittest.skipIf(__version__ < (1, 3), "not supported in this library version")
    def test_format(self):
        # Tests that work for only a certain version of the library.
        pass

    @unittest.skipUnless(sys.platform.startswith("win"), "requires Windows")
    def test_windows_support(self):
        # windows specific testing code
        pass

    def test_catchExcept(self):
        try:
            1 / 0
        except:
            raise unittest.SkipTest("skipping because ...")
        self.assertEqual(True)
```

testExpectedFailure.py:
```python
import unittest

class ExpectedFailureTestCase(unittest.TestCase):
    @unittest.expectedFailure
    def test_fail(self):
        self.assertEqual(1, 0, "broken")
```

測試結果：
```shell
$ python -m unittest discover -v -p "test*.py"
test_fail (testExpectedFailure.ExpectedFailureTestCase) ... expected failure
test_catchExcept (testSkip.TestSkipCase) ... skipped 'skipping because ...'
test_format (testSkip.TestSkipCase) ... skipped 'not supported in this library version'
test_nothing (testSkip.TestSkipCase) ... skipped 'demonstrating skipping'
test_windows_support (testSkip.TestSkipCase) ... skipped 'requires Windows'

----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK (skipped=4, expected failures=1)
```

以下修飾詞 (decorator) 用來忽略或預期失敗：

| 修飾詞 | 說明 |
|--------|------|
| `@unittest.skip(reason)` | 無條件忽略測試。reason 說明為何要忽略測試 |
| `@unittest.skipIf(condition, reason)` | 如果條件成立，則忽略測試 |
| `@unittest.skipUnless(condition, reason)` | 除非條件成立，否則忽略測試 |
| `@unittest.expectedFailure` | 標記測試為預期錯誤。執行時如果測試失敗，結果不算失敗 |
| `exception unittest.SkipTest(reason)` | 產生例外，忽略測試 |

## 測試方法

| 方法 | 檢查 |
|------|------|
| `assertEqual(a, b)` | a == b |
| `assertNotEqual(a, b)` | a != b |
| `assertTrue(x)` | bool(x) is True |
| `assertFalse(x)` | bool(x) is False |
| `assertIs(a, b)` | a is b |
| `assertIsNot(a, b)` | a is not b |
| `assertIsNone(x)` | x is None |
| `assertIsNotNone(x)` | x is not None |
| `assertIn(a, b)` | a in b |
| `assertNotIn(a, b)` | a not in b |
| `assertIsInstance(a, b)` | isinstance(a, b) |
| `assertNotIsInstance(a, b)` | not isinstance(a, b) |


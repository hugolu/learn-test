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

TestStringMethods:
```python
import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main()
```

- `test_upper` 測試 `upper()` 函數是否正確運作
- `test_isupper` 測試 `isupper()` 函數是否正確運作
- `test_split` 測試 `split()` 函數是否正確運作，並驗證例外是否發生

執行結果：
```shell
$ python TestStringMethods.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK
$ python TestStringMethods.py -v                        # 使用參數 -v 提供測試細節
test_isupper (__main__.TestStringMethods) ... ok
test_split (__main__.TestStringMethods) ... ok
test_upper (__main__.TestStringMethods) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.000s

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
$ $ python -m unittest TestArithmetic                   # 測試 TestArithmetic 模組，不含副檔名 (.py)
....
----------------------------------------------------------------------
Ran 4 tests in 0.000s

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

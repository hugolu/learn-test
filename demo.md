# Demo of BDD/TDD/CI on Django

## 前言

本來想用網站帳號註冊與登入來示範 TDD/BDD，但是
- 帳號檢查的邏輯太簡單，很難示範 TDD
- Behave-django 做得太好了，Model 根本不需要 mock

要找出一個範例會複雜到需要拆成 features, steps, interfaces, implementation of [SUT](http://xunitpatterns.com/SUT.html), 還有要切割依賴的 [DOC](http://xunitpatterns.com/DOC.html)，同時又必須簡單到範例可以塞進一張投影片。幾經考量，轉而想使用解析字串的計算機(類似工程用計算機)做範例。

計算機須滿足 [四則運算規則](https://zh.wikipedia.org/wiki/%E5%9B%9B%E5%88%99%E8%BF%90%E7%AE%97)
- 由左而右計算
- 先括號，再× ÷，後 + −（先乘除後加減）
- 先算內括號，再算外括號
- [運算子優先順序](https://zh.wikipedia.org/wiki/%E9%81%8B%E7%AE%97%E6%AC%A1%E5%BA%8F)
- [加法交換律](https://zh.wikipedia.org/wiki/%E4%BA%A4%E6%8F%9B%E5%BE%8B): "3 + 4 = 4 + 3"
- [加法結合律](https://zh.wikipedia.org/wiki/%E7%BB%93%E5%90%88%E5%BE%8B): "(5+2) + 1 = 5 + (2+1) = 8"
- [乘法交換律](https://zh.wikipedia.org/wiki/%E4%BA%A4%E6%8F%9B%E5%BE%8B): "2 × 5 = 5 × 2"
- [乘法結合律](https://zh.wikipedia.org/wiki/%E7%BB%93%E5%90%88%E5%BE%8B): "(5x2) x 3 = 5 x (2x3) = 30"
- [乘法分配律](https://zh.wikipedia.org/wiki/%E5%88%86%E9%85%8D%E5%BE%8B): "2 x(1+3) = (2x1) + (2x3)"

## 設定環境

```shell
vagrant@debian:~$ cd myWorkspace/venv/
$ source venv/bin/activate
(venv) vagrant@debian:~/myWorkspace$
```
- 以下範例省略提示符號`$`前所有文字

### 安裝 Djando 專案

```shell
$ django-admin startproject demo
$ tree demo/
demo/
├── demo
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
$ cd demo
```

### 建立 Calculator App

```shell
$ python manage.py startapp calc
$ tree calc
calc
├── admin.py
├── apps.py
├── __init__.py
├── migrations
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
```

### 新增 Calculator App

修改 demo/settings.py
```python
INSTALLED_APPS = [
    'behave_django',
    ...
]
```

## 藉由 BDD 引導，定義特徵與步驟

### 一開始什麼都沒有

先什麼都不做，跑一下 behave 看看發生什麼事情

第一次執行 behave
```shell
$ python manage.py behave
Creating test database for alias 'default'...
ConfigError: No steps directory in "/home/vagrant/myWorkspace/demo/features"
Destroying test database for alias 'default'...
```
- 溫馨提示: 缺少 features/steps 目錄

### 建立 features/steps 目錄

```shell
$ mkdir -p features/steps
```

第二次執行 behave
```shell
$ python manage.py behave
Creating test database for alias 'default'...
ConfigError: No feature files in "/home/vagrant/myWorkspace/demo/features"
Destroying test database for alias 'default'...
```
- 溫馨提示: 還沒有定義特徵 (features)

### 建立 calc 的特徵描述檔

產生檔案 features/calc.feature:
```python
#file: features/calc.feature

Feature: Web calculator

    As a student
    In order to finish my homework
    I want to do arithmatical operations

    Scenario: add two numbers
        Given I enter "1+1"
         When I press "=" button
         Then I get the answer "2"
```

第三次執行 behave
```shell
$ python manage.py behave --dry-run

Feature: Web calculator # features/calc.feature:3
  As a student
  In order to finish my homework
  I want to do arithmatical operations
  Scenario: add two numbers   # features/calc.feature:9
    Given I enter "3+2"       # None
    When I press "=" button   # None
    Then I get the answer "5" # None

0 features passed, 0 failed, 0 skipped, 1 untested
0 scenarios passed, 0 failed, 0 skipped, 1 untested
0 steps passed, 0 failed, 0 skipped, 3 undefined
Took 0m0.000s

You can implement step definitions for undefined steps with these snippets:

@given(u'I enter "3+2"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I enter "3+2"')

@when(u'I press "=" button')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I press "=" button')

@then(u'I get the answer "5"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I get the answer "5"')
```
- 溫馨提示: 還沒有定義步驟 (steps)，這些 snippets 可以拿去用

### 建立 calc 的步驟定義檔

產生檔案 features/steps/calc.py:
```python
@given(u'I enter "3+2"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I enter "1+1"')

@when(u'I press "=" button')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I press "=" button')

@then(u'I get the answer "5"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I get the answer "2"')
```

第四次執行 behave
```shell
$ python manage.py behave --dry-run

Feature: Web calculator # features/calc.feature:3
  As a student
  In order to finish my homework
  I want to do arithmatical operations
  Scenario: add two numbers   # features/calc.feature:9
    Given I enter "3+2"       # None
    When I press "=" button   # None
    Then I get the answer "5" # None

0 features passed, 0 failed, 0 skipped, 1 untested
0 scenarios passed, 0 failed, 0 skipped, 1 untested
0 steps passed, 0 failed, 0 skipped, 0 undefined, 3 untested
Took 0m0.000s
```
- 溫馨提示: 一個 feature、一個 scenario、三個 steps 沒有測試

### 再增加一個 scenario

修改 features/calc.feature，增加以下程式片段:
```python
    Scenario: subtract two numbers
        Given I enter "3-2"
         When I press "=" button
         Then I get the answer "1"
```

第五次執行 behave
```shell
$ python manage.py behave --dry-run

Feature: Web calculator # features/calc.feature:3
  As a student
  In order to finish my homework
  I want to do arithmatical operations
  Scenario: add two numbers   # features/calc.feature:9
    Given I enter "3+2"       # None
    When I press "=" button   # None
    Then I get the answer "5" # None

  Scenario: subtract two numbers  # features/calc.feature:14
    Given I enter "3-2"           # None
    When I press "=" button       # None
    Then I get the answer "1"     # None

0 features passed, 0 failed, 0 skipped, 1 untested
0 scenarios passed, 0 failed, 0 skipped, 2 untested
0 steps passed, 0 failed, 0 skipped, 2 undefined, 4 untested
Took 0m0.000s

You can implement step definitions for undefined steps with these snippets:

@given(u'I enter "3-2"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I enter "3-2"')

@then(u'I get the answer "1"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I get the answer "1"')
```
- 溫馨提示: 有些 features, scenarios, steps 沒有測試；有 steps 沒定義，可使用提供的 snippets

### 修改 calc 的步驟定義檔

修改檔案 features/steps/calc.py，增加以下程式片段:
```python
@given(u'I enter "3-2"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I enter "3-2"')

@then(u'I get the answer "1"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I get the answer "1"')
```

第六次執行 behave
```shell
$ python manage.py behave --dry-run

Feature: Web calculator # features/calc.feature:3
  As a student
  In order to finish my homework
  I want to do arithmatical operations
  Scenario: add two numbers   # features/calc.feature:9
    Given I enter "3+2"       # None
    When I press "=" button   # None
    Then I get the answer "5" # None

  Scenario: subtract two numbers  # features/calc.feature:14
    Given I enter "3-2"           # None
    When I press "=" button       # None
    Then I get the answer "1"     # None

0 features passed, 0 failed, 0 skipped, 1 untested
0 scenarios passed, 0 failed, 0 skipped, 2 untested
0 steps passed, 0 failed, 0 skipped, 0 undefined, 6 untested
Took 0m0.000s
```
- 溫馨提示: 有些 features, scenarios, steps 沒有測試

### 重構步驟定義檔 - 使用變數

修改檔案 features/steps/calc.py
```python
@given(u'I enter {expr}')
def step_impl(context, expr):
    raise NotImplementedError(u'STEP: Given I enter {expr}')

@when(u'I press "=" button')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I press "=" button')

@then(u'I get the answer {answer}')
def step_impl(context, answer):
    raise NotImplementedError(u'STEP: Then I get the answer {answer}')
```

第七次執行 behave
```shell
$ python manage.py behave --dry-run

Feature: Web calculator # features/calc.feature:3
  As a student
  In order to finish my homework
  I want to do arithmatical operations
  Scenario: add two numbers   # features/calc.feature:9
    Given I enter "3+2"       # None
    When I press "=" button   # None
    Then I get the answer "5" # None

  Scenario: subtract two numbers  # features/calc.feature:14
    Given I enter "3-2"           # None
    When I press "=" button       # None
    Then I get the answer "1"     # None

0 features passed, 0 failed, 0 skipped, 1 untested
0 scenarios passed, 0 failed, 0 skipped, 2 untested
0 steps passed, 0 failed, 0 skipped, 0 undefined, 6 untested
Took 0m0.000s
```
- 步驟檔使用變數，定義一個 step 能適用多個 scenarios

### 重構特徵描述檔 - 合併場景

修改 features/calc.feature，使用 `Scenario Outline` 合併加法、減法場景，並增加更多場景與錯誤處理
```python
    Scenario Outline: do simple operations
        Given I enter <expression>
         When I press "=" button
         Then I get the answer <answer>

        Examples:
            | expression    | answer        |
            | 3 + 2         | 5             |
            | 3 - 2         | 1             |
            | 3 * 2         | 6             |
            | 3 / 2         | 1.5           |
            | 3 +-*/        | Invalid Input |
            | hello world   | Invalid Input |
```

第八次執行 behave
```shell
$ python manage.py behave --dry-run

Feature: Web calculator # features/calc.feature:3
  As a student
  In order to finish my homework
  I want to do arithmatical operations
  Scenario Outline: do simple operations -- @1.1   # features/calc.feature:16
    Given I enter 3 + 2                            # None
    When I press "=" button                        # None
    Then I get the answer 5                        # None

  Scenario Outline: do simple operations -- @1.2   # features/calc.feature:17
    Given I enter 3 - 2                            # None
    When I press "=" button                        # None
    Then I get the answer 1                        # None

  Scenario Outline: do simple operations -- @1.3   # features/calc.feature:18
    Given I enter 3 * 2                            # None
    When I press "=" button                        # None
    Then I get the answer 6                        # None

  Scenario Outline: do simple operations -- @1.4   # features/calc.feature:19
    Given I enter 3 / 2                            # None
    When I press "=" button                        # None
    Then I get the answer 1.5                      # None

  Scenario Outline: do simple operations -- @1.5   # features/calc.feature:20
    Given I enter 3 +-*/ 2                         # None
    When I press "=" button                        # None
    Then I get the answer Invalid Input            # None

  Scenario Outline: do simple operations -- @1.6   # features/calc.feature:21
    Given I enter hello world                      # None
    When I press "=" button                        # None
    Then I get the answer Invalid Input            # None

0 features passed, 0 failed, 0 skipped, 1 untested
0 scenarios passed, 0 failed, 0 skipped, 6 untested
0 steps passed, 0 failed, 0 skipped, 0 undefined, 18 untested
Took 0m0.000s
```
- 溫馨提示: 更多 features, scenarios, steps 沒有測試

### 增加更多特徵

修改 features/calc.feature，使特徵滿足
[加法/乘法交換律](https://zh.wikipedia.org/wiki/%E4%BA%A4%E6%8F%9B%E5%BE%8B)、[加法/乘法結合律](https://zh.wikipedia.org/wiki/%E7%BB%93%E5%90%88%E5%BE%8B)、、[乘法分配律](https://zh.wikipedia.org/wiki/%E5%88%86%E9%85%8D%E5%BE%8B)
```python
    Scenario Outline: satisfy commutative property
         When I enter <expression1> first
          And I enter <expression2> again
         Then I get the same answer

        Examples:
            | expression1   | expression2   |
            | 3 + 4         | 4 + 3         |
            | 2 * 5         | 5 * 2         |

    Scenario Outline: satisfy associative property
         When I enter <expression1> first
          And I enter <expression2> again
         Then I get the same answer

        Examples:
            | expression1   | expression2   |
            | (2 + 3) + 4   | 2 + (3 + 4)   |
            | 2 * (3 * 4)   | (2 * 3) * 4   |

    Scenario Outline: satisfy distributive property
         When I enter <expression1> first
          And I enter <expression2> again
         Then I get the same answer

        Examples:
            | expression1   | expression2   |
            | 2 * (1 + 3)   | (2*1) + (2*3) |
```

第九次執行 behave
```shell
$ python manage.py behave --dry-run

Feature: Web calculator # features/calc.feature:3
  As a student
  In order to finish my homework
  I want to do arithmatical operations
  Scenario Outline: do simple operations -- @1.1   # features/calc.feature:16
    Given I enter 3 + 2                            # None
    When I press "=" button                        # None
    Then I get the answer 5                        # None

  ...(略)

0 features passed, 0 failed, 0 skipped, 1 untested
0 scenarios passed, 0 failed, 0 skipped, 11 untested
0 steps passed, 0 failed, 0 skipped, 15 undefined, 18 untested
Took 0m0.000s

You can implement step definitions for undefined steps with these snippets:

@when(u'I enter 3 + 4 first')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I enter 3 + 4 first')

@when(u'I enter 4 + 3 again')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I enter 4 + 3 again')

@then(u'I get the same answer')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I get the same answer')

@when(u'I enter 2 * 5 first')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I enter 2 * 5 first')

@when(u'I enter 5 * 2 again')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I enter 5 * 2 again')

@when(u'I enter (2 + 3) + 4 first')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I enter (2 + 3) + 4 first')

@when(u'I enter 2 + (3 + 4) again')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I enter 2 + (3 + 4) again')

@when(u'I enter 2 * (3 * 4) first')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I enter 2 * (3 * 4) first')

@when(u'I enter (2 * 3) * 4 again')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I enter (2 * 3) * 4 again')

@when(u'I enter 2 * (1 + 3) first')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I enter 2 * (1 + 3) first')

@when(u'I enter (2*1) + (2*3) again')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I enter (2*1) + (2*3) again')
```

### 增加步驟

```python
@when(u'I enter {expr1} first')
def step_impl(context, expr1):
    raise NotImplementedError(u'STEP: When I enter {expr} first')

@when(u'I enter {expr2} again')
def step_impl(context, expr2):
    raise NotImplementedError(u'STEP: When I enter {expr2} again')

@then(u'I get the same answer')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I get the same answer')
```

第十次執行 behave，這次不用 `--dry-run` 參數
```shell
$ python manage.py behave

Creating test database for alias 'default'...
Feature: Web calculator # features/calc.feature:3
  As a student
  In order to finish my homework
  I want to do arithmatical operations
  Scenario Outline: do simple operations -- @1.1   # features/calc.feature:16
    Given I enter 3 + 2                            # features/steps/calc.py:1 0.000s
      Traceback (most recent call last):
        File "/home/vagrant/myWorkspace/venv/lib/python3.5/site-packages/behave/model.py", line 1456, in run
          match.run(runner.context)
        File "/home/vagrant/myWorkspace/venv/lib/python3.5/site-packages/behave/model.py", line 1903, in run
          self.func(context, *args, **kwargs)
        File "/home/vagrant/.pyenv/versions/3.5.1/lib/python3.5/contextlib.py", line 77, in __exit__
          self.gen.throw(type, value, traceback)
        File "/home/vagrant/myWorkspace/venv/lib/python3.5/site-packages/behave/runner.py", line 162, in user_mode
          yield
        File "/home/vagrant/myWorkspace/venv/lib/python3.5/site-packages/behave/model.py", line 1903, in run
          self.func(context, *args, **kwargs)
        File "features/steps/calc.py", line 3, in step_impl
          raise NotImplementedError(u'STEP: Given I enter {expr}')
      NotImplementedError: STEP: Given I enter {expr}

    When I press "=" button                        # None
    Then I get the answer 5                        # None

...(略)

Failing scenarios:
  features/calc.feature:16  do simple operations -- @1.1
  features/calc.feature:17  do simple operations -- @1.2
  features/calc.feature:18  do simple operations -- @1.3
  features/calc.feature:19  do simple operations -- @1.4
  features/calc.feature:20  do simple operations -- @1.5
  features/calc.feature:21  do simple operations -- @1.6
  features/calc.feature:30  satisfy commutative property -- @1.1
  features/calc.feature:31  satisfy commutative property -- @1.2
  features/calc.feature:40  satisfy associative property -- @1.1
  features/calc.feature:41  satisfy associative property -- @1.2
  features/calc.feature:50  satisfy distributive property -- @1.1

0 features passed, 1 failed, 0 skipped
0 scenarios passed, 11 failed, 0 skipped
0 steps passed, 11 failed, 22 skipped, 0 undefined
Took 0m0.003s
Destroying test database for alias 'default'...
```
- 溫馨提示: 一堆 features, scenarios, steps 失敗

### 重構特徵描述檔 - 移除 `NotImplementedError`

```python
from cala.calculator import Calculator

@given(u'I enter {expr}')
def step_impl(context, expr):
    context.expr = expr

@when(u'I press "=" button')
def step_impl(context):
    calc = Calculator()
    context.answer = calc.evalString(context.expr)

@then(u'I get the answer {answer}')
def step_impl(context, answer):
    try:
        ans = float(answer)
    except ValueError:
        ans = answer

    assert context.answer == ans

@when(u'I enter {expr1} first')
def step_impl(context, expr1):
    calc = Calculator()
    context.answer1 = calc.evalString(expr1)

@when(u'I enter {expr2} again')
def step_impl(context, expr2):
    calc = Calculator()
    context.answer2 = calc.evalString(expr2)

@then(u'I get the same answer')
def step_impl(context):
    assert context.answer1 == context.answer2
```

第十一次執行 behave
```shell
$ python manage.py behave

Creating test database for alias 'default'...
Exception ImportError: No module named 'calc.calculator'; 'calc' is not a package
Traceback (most recent call last):
  ...(略)
  File "/home/vagrant/myWorkspace/demo/features/steps/calc.py", line 1, in <module>
    from calc.calculator import Calculator
ImportError: No module named 'calc.calculator'; 'calc' is not a package
```
- 溫馨提示: No module named 'calc.calculator'; 'calc' is not a package

### 修改專案設定

修改 demo/settings.py，增加 `calc` App
```python
INSTALLED_APPS = [
    ...
    'calc',
]
```

第十二次執行 behave
```shell
$ python manage.py behave

Creating test database for alias 'default'...
Exception ImportError: No module named 'calc.calculator'
Traceback (most recent call last):
  ...(略)
  File "features/steps/calc.py", line 1, in <module>
    from calc.calculator import Calculator
ImportError: No module named 'calc.calculator'
```
- 溫馨提示: No module named 'calc.calculator'

### 增加模組 calc

```shell
$ touch calc/calculator.py
```

第十三次執行 behave
```shell
$ python manage.py behave

Creating test database for alias 'default'...
Exception ImportError: cannot import name 'Calculator'
Traceback (most recent call last):
  ...(略)
  File "features/steps/calc.py", line 1, in <module>
    from calc.calculator import Calculator
ImportError: cannot import name 'Calculator'
```
- 溫馨提示: cannot import name 'Calculator'

### 增加 `Calculator` 類別

修改 calc/calculator.py，增加 `Calculator` 類別，並提供 `evalString` 方法
```python
class Calculator:

    def evalString(self, string):
        return 0
```

第十四次執行 behave
```shell
$ python manage.py behave

Creating test database for alias 'default'...
Feature: Web calculator # features/calc.feature:3
  As a student
  In order to finish my homework
  I want to do arithmatical operations
  Scenario Outline: do simple operations -- @1.1   # features/calc.feature:16
    Given I enter 3 + 2                            # features/steps/calc.py:3 0.000s
    When I press "=" button                        # features/steps/calc.py:7 0.000s
    Then I get the answer 5                        # features/steps/calc.py:12 0.000s
      Traceback (most recent call last):
        File "/home/vagrant/myWorkspace/venv/lib/python3.5/site-packages/behave/model.py", line 1456, in run
          match.run(runner.context)
        File "/home/vagrant/myWorkspace/venv/lib/python3.5/site-packages/behave/model.py", line 1903, in run
          self.func(context, *args, **kwargs)
        File "features/steps/calc.py", line 19, in step_impl
          assert context.answer == ans
      AssertionError

...(略)

Failing scenarios:
  features/calc.feature:16  do simple operations -- @1.1
  features/calc.feature:17  do simple operations -- @1.2
  features/calc.feature:18  do simple operations -- @1.3
  features/calc.feature:19  do simple operations -- @1.4
  features/calc.feature:20  do simple operations -- @1.5
  features/calc.feature:21  do simple operations -- @1.6

0 features passed, 1 failed, 0 skipped
5 scenarios passed, 6 failed, 0 skipped
27 steps passed, 6 failed, 0 skipped, 0 undefined
Took 0m0.005s
Destroying test database for alias 'default'...
```
- 溫馨提示: 有些成功、有些失敗 (因為還沒實作功能)
- 可以開始實作 `Calculator` 了

## 藉由 TDD 引導，實作底層功能

開始開發 `Calculator` 功能之前，先把剛剛的程式碼放到 git repository
```shell
$ git init
```

新增 .gitignore 檔案，避免某些檔案加入 git repository
```
__pycache__
db.sqlite3
.python-version
*.pyc
.*.swp
reports/
```

```shell
$ git add .
$ git commit -m "init project"
```

### 新增第一個測試案例

修改 calc/tests.py
```python
from django.test import TestCase
from calc.calculator import Calculator

# Create your tests here.
class TestCalculator(TestCase):

    def setUp(self):
        self.calc = Calculator()

    def test_evalString(self):
        evalString = self.calc.evalString
        self.assertEqual(evalString('0'), 0)
```

執行 unittest
```shell
$ python manage.py test -v2
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Operations to perform:
  Synchronize unmigrated apps: behave_django, messages, django_jenkins, staticfiles
  Apply all migrations: sessions, admin, auth, contenttypes
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  ...(略)
test_evalString (calc.tests.TestCalculator) ... ok

----------------------------------------------------------------------
Ran 1 test in 0.002s

OK
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
```
- 溫馨提示: 剛剛最簡單的測試 `test_evalString` 通過

把通過測試的程式碼與測試程式碼放上 git repository
```shell
$ git add .
$ git commit -m "add test_evalString"
```

### 再多一點點測試

修改 calc/tests.py
```python
    def test_evalString(self):
        evalString = self.calc.evalString
        self.assertEqual(evalString('0'), 0)
        self.assertEqual(evalString('0'), 1)
```

執行 unittest
```shell
$ python manage.py test -v2
...（略)

test_evalString (calc.tests.TestCalculator) ... FAIL

======================================================================
FAIL: test_evalString (calc.tests.TestCalculator)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/vagrant/myWorkspace/demo/calc/tests.py", line 13, in test_evalString
    self.assertEqual(evalString('0'), 1)
AssertionError: 0 != 1

----------------------------------------------------------------------
Ran 1 test in 0.002s

FAILED (failures=1)
```
- 溫馨提示: `test_evalString` 測試失敗，快去修改 `Calculator`

### 插播 pyparsing

接下來會使用 pyparsing 來解析輸入字串，把字串變成“數字”與“運算符號”，然後根據運算符號執行正確的計算。

例如，輸入 `3+2`，解析字串後得到 `exprStack=['3', '2', '+']`，從 `exprStack` 取出 (pop) 元素 `+`，因為 `+` 是運算符號，要再取出兩個運算元 `2` 與 `3` (依照取出順序)，然後呼叫 `+` 符號對應的函數 `add(3, 2)`，最後得答案 `5`。

> 細節請參考 pyparsing [說明](pyparsing.md)與[範例](pyparsing_exercise.md)

### 修改 `Calculator` - 增加解析字串能力

修改 calc/tests.py，增加 `parseString` 測試
```python
    def test_parseString(self):
        parseString = self.calc.parseString
        self.assertEqual(parseString('0'), ['0'])
        self.assertEqual(parseString('1'), ['1'])
```

執行 unittest
```shell
$ python manage.py test
...(略)
======================================================================
ERROR: test_parseString (calc.tests.TestCalculator)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/vagrant/myWorkspace/demo/calc/tests.py", line 11, in test_parseString
    parseString = self.calc.parseString
AttributeError: 'Calculator' object has no attribute 'parseString'
```
- 溫馨提示: 'Calculator' object has no attribute 'parseString'

修改 calc/calculator.py，增加 `parseString` 方法滿足測試
```python
from pyparsing import nums, Word, StringEnd

"""
integer :: '0'...'9'*
expr    :: integer
"""

class Calculator:

    def __init__(self):
        self.exprStack = []

        integer = Word(nums)
        self.expr = integer + StringEnd()

    def parseString(self, string):
        self.exprStack = []
        return self.expr.parseString(string).asList()

    def evalString(self, string):
        return 0
```
- 增加 `parseString` 解析功能

執行 unittest，測試 `parseString` 方法
```shell
$ python manage.py test -v2
...(略)
test_evalString (calc.tests.TestCalculator) ... FAIL
test_parseString (calc.tests.TestCalculator) ... ok
```
- 溫馨提示: `test_parseString` 測試通過，繼續努力

### 修改 `Calculator` - 增加解析 `exprStack` 能力

修改 calc/tests.py，增加 `evalStack` 測試
```python
    def test_evalStack(self):
        evalStack = self.calc.evalStack
        self.assertEqual(evalStack(['0']), 0)
        self.assertEqual(evalStack(['1']), 1)
```

執行 unittest
```shell
$ python manage.py test
...(略)
======================================================================
ERROR: test_evalStack (calc.tests.TestCalculator)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/home/vagrant/myWorkspace/demo/calc/tests.py", line 16, in test_evalStack
    evalStack = self.calc.evalStack
AttributeError: 'Calculator' object has no attribute 'evalStack'
```
- 溫馨提示: 'Calculator' object has no attribute 'evalStack'

修改 calc/calculator.py，增加 `evalStack` 方法滿足測試
```python
class Calculator:

    ...(略)
    
    def evalStack(self, stack):
        op = stack.pop()
        return float(op)
```

執行 unittest，測試 `evalStack` 方法
```shell
$ python manage.py test -v2
...(略)
test_evalStack (calc.tests.TestCalculator) ... ok
test_evalString (calc.tests.TestCalculator) ... FAIL
test_parseString (calc.tests.TestCalculator) ... ok
```
- 溫馨提示: `test_evalStack` 測試通過，快讓 `test_evalString` 通過測試吧

### 修改 `Calculator` - 完善解析字串能力

這次不修改 calc/tests.py，沿用裡面的測試

修改 calc/calculator.py，完善 `parseString` 方法滿足測試
```python
class Calculator:

    def __init__(self):
        self.exprStack = []

        def pushStack(s, l, t):
            self.exprStack.append(t[0])

        integer = Word(nums).addParseAction(pushStack)
        self.expr = integer + StringEnd()

    ...(略)
    
    def evalString(self, string):
        self.parseString(string)
        return self.evalStack(self.exprStack)
```

執行 unittest，測試 `evalString` 方法
```shell
$ python manage.py test -v2
...(略)
test_evalStack (calc.tests.TestCalculator) ... ok
test_evalString (calc.tests.TestCalculator) ... ok
test_parseString (calc.tests.TestCalculator) ... ok
```
- 溫馨提示: `test_evalStack`, `test_evalString`, `test_parseString` 測試通過，先 git commit 吧

```shell
$ git add .
$ git commit -m "test evalStack, evalString, parseString: ok"
```

### 修改 `Calculator` - 增加錯誤處理

修改 calc/tests.py，增加輸入錯誤測試
```python
    def test_invalid_input(self):
        evalString = self.calc.evalString
        self.assertEqual(evalString('hello world'), 'Invalid Input')
```

執行 unittest，測試 `evalString` 方法
```shell
$ python manage.py test
..E.
======================================================================
ERROR: test_invalid_input (calc.tests.TestCalculator)
----------------------------------------------------------------------
Traceback (most recent call last):
  ...(略)
  File "/home/vagrant/myWorkspace/venv/lib/python3.5/site-packages/pyparsing.py", line 1936, in parseImpl
    raise ParseException(instring, loc, self.errmsg, self)
pyparsing.ParseException: Expected W:(0123...) (at char 0), (line:1, col:1)

```
- 溫馨提示: 發生 `ParseException`，快去處理

修改 calc/calculator.py，完善 `parseString` 方法滿足測試
```python
from pyparsing import nums, Word, StringEnd, ParseException

class Calculator:

    ...(略)
    
    def evalString(self, string):
        try:
            self.parseString(string)
            return self.evalStack(self.exprStack)
        except ParseException:
            return 'Invalid Input'
```

執行 unittest，測試 `evalString` 方法
```shell
$ python manage.py test
Creating test database for alias 'default'...
....
----------------------------------------------------------------------
Ran 4 tests in 0.005s

OK
Destroying test database for alias 'default'...
```
- 溫馨提示: 測試全部通過，先 git commit 吧

```shell
$ git add .
$ git commit -m "handle ParseException"
```












----
### 環境設定

開發環境相關設定，請參考 [Django 設定環境](django.md#設定環境)

### Jenkins 設定

Jenkins 伺服器建置說明，請參考 [Jenkins](jenkins.md)、[django-jenkins](django-jenkins.md) 

開啟瀏覽器，連接 http://192.168.33.10:8000/ ([虛擬機](environment.md))
- Jenkins 管理首頁
    - New Item
        - Item name: `demo`
            - [x] Freestyle project
    - Source Code Management
        - [x] Git
            - Repository URL: `file:///home/vagrant/myWorkspace/demo`
    - Build Triggers
        - [x] Poll SCM
            - Schedule: `* * * * *`
    - Build Environment
        - [x] pyenv build wrapper
            - The Python version: `3.5.1`
    - Build
        - [x] Execute shell
            - Command: [shell command](#shell-command)
    - Post-build Actions
        - [x] Publish Cobertura Coverage Report
            - Cobertura xml report pattern: `reports/coverage.xml`
        - [x] Publish JUnit test result report
            - Test report XMLs: `reports/junit.xml`
        - [x] Report Violations
            - pylint: `reports/pylint.report`
    - Save 

#### shell command
```
PATH=$WORKSPACE/venv/bin:/usr/local/bin:$PATH

if [ ! -d "venv" ]; then
        virtualenv venv
fi
. venv/bin/activate
pip install -r requirements.txt

python manage.py jenkins --enable-coverage
```

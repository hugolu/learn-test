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

## 安裝 Djando 專案

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

## 建立 Calculator App

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

## 新增 Calculator App

修改 demo/settings.py
```python
INSTALLED_APPS = [
    'behave_django',
    ...
]
```

## 第一次執行 behave

```shell
$ python manage.py behave
Creating test database for alias 'default'...
ConfigError: No steps directory in "/home/vagrant/myWorkspace/demo/features"
Destroying test database for alias 'default'...
```
- 溫馨提示: 缺少 features/steps 目錄

## 建立 features/steps 目錄

```shell
$ mkdir -p features/steps
```

## 第二次執行 behave

```shell
$ python manage.py behave
Creating test database for alias 'default'...
ConfigError: No feature files in "/home/vagrant/myWorkspace/demo/features"
Destroying test database for alias 'default'...
```
- 溫馨提示: 還沒有定義特徵 (features)

## 建立 calc 的特徵描述檔

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

## 第三次執行 behave

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

## 建立 calc 的步驟定義檔

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

## 第四次執行 behave

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

## 再增加一個 scenario

修改 features/calc.feature，增加以下程式片段:
```python
    Scenario: subtract two numbers
        Given I enter "3-2"
         When I press "=" button
         Then I get the answer "1"
```

## 第五次執行 behave

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

## 修改 calc 的步驟定義檔

修改檔案 features/steps/calc.py，增加以下程式片段:
```python
@given(u'I enter "3-2"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I enter "3-2"')

@then(u'I get the answer "1"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I get the answer "1"')
```

## 第六次執行 behave

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

## 重構步驟定義檔 - 使用變數

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

## 第七次執行 behave

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

## 重構特徵描述檔 - 合併場景

修改 features/calc.feature，使用 `Scenario Outline` 合併加法、減法場景，並增加更多場景
```python
    Scenario Outline: do simple operations
        Given I enter <expression>
         When I press "=" button
         Then I get the answer <answer>

        Examples:
            | expression    | answer    |
            | 3 + 2         | 5         |
            | 3 - 2         | 1         |
            | 3 * 2         | 6         |
            | 3 / 2         | 1.5       |
```

## 第八次執行 behave

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

0 features passed, 0 failed, 0 skipped, 1 untested
0 scenarios passed, 0 failed, 0 skipped, 4 untested
0 steps passed, 0 failed, 0 skipped, 0 undefined, 12 untested
Took 0m0.000s
```
- 溫馨提示: 更多 features, scenarios, steps 沒有測試


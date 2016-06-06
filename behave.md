# Behave

參考連結:

- [Behave official site](http://pythonhosted.org/behave/)
- [behave Examples and Tutorials](https://jenisys.github.io/behave.example/index.html)

## 透過範例快速瀏覽

參考：[Python BDD自动化测试框架初探](http://lovesoo.org/python-bdd-exploration-of-the-automated-testing-framework.html)，計算 fibonacci 數列

首先建立目錄結構
```shell
$ mkdir fib
$ cd fib
$ mkdir -p features/steps
```

描述 feature 的長相
```python
# file:features/fib.feature
Feature:Calc Fib
    In order to introduce Behave
    We calc fib as example

  Scenario: Calc fib number
     Given we have the number 10
      when we calc the fib
      then we get the fib number 55
```

執行 beheve
```shell
$ behave
Feature: Calc Fib # features/fib.feature:2
  In order to introduce Behave
  We calc fib as example
  Scenario: Calc fib number       # features/fib.feature:6
    Given we have the number 10   # None
    When we calc the fib          # None
    Then we get the fib number 55 # None


Failing scenarios:
  features/fib.feature:6  Calc fib number

0 features passed, 1 failed, 0 skipped
0 scenarios passed, 1 failed, 0 skipped
0 steps passed, 0 failed, 0 skipped, 3 undefined
Took 0m0.000s

You can implement step definitions for undefined steps with these snippets:

@given(u'we have the number 10')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given we have the number 10')

@when(u'we calc the fib')
def step_impl(context):
    raise NotImplementedError(u'STEP: When we calc the fib')

@then(u'we get the fib number 55')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then we get the fib number 55')
```

把 behave 提供的 snippets 拿來改成 steps
```python
# file:features/steps/step_fib.py
# ----------------------------------------------------------------------------
# STEPS:
# ----------------------------------------------------------------------------
@given(u'we have the number 10')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given we have the number 10')

@when(u'we calc the fib')
def step_impl(context):
    raise NotImplementedError(u'STEP: When we calc the fib')

@then(u'we get the fib number 55')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then we get the fib number 55')
```

再跑一次 behave
```shell
$ behave
Feature: Calc Fib # features/fib.feature:2
  In order to introduce Behave
  We calc fib as example
  Scenario: Calc fib number       # features/fib.feature:6
    Given we have the number 10   # features/steps/step_fib.py:2 0.000s
      Traceback (most recent call last):
        File "/usr/local/lib/python2.6/dist-packages/behave/model.py", line 1456, in run
          match.run(runner.context)
        File "/usr/local/lib/python2.6/dist-packages/behave/model.py", line 1903, in run
          self.func(context, *args, **kwargs)
        File "features/steps/step_fib.py", line 4, in step_impl
          raise NotImplementedError(u'STEP: Given we have the number 10')
      NotImplementedError: STEP: Given we have the number 10

    When we calc the fib          # None
    Then we get the fib number 55 # None


Failing scenarios:
  features/fib.feature:6  Calc fib number

0 features passed, 1 failed, 0 skipped
0 scenarios passed, 1 failed, 0 skipped
0 steps passed, 1 failed, 2 skipped, 0 undefined
Took 0m0.000s
```

修改 steps，並實作出 fibs
```python
# file:features/steps/step_fib.py
# ----------------------------------------------------------------------------
# PROBLEM DOMAIN:
# ----------------------------------------------------------------------------
def fibs(num):
    a = b = 1
    for i in range(num):
        yield a
        a, b = b, a + b
# ----------------------------------------------------------------------------
# STEPS:
# ----------------------------------------------------------------------------
@given(u'we have the number 10')
def step_impl(context):
    context.fib_number = 10

@when(u'we calc the fib')
def step_impl(context):
    context.fib_number=list(fibs(context.fib_number))[-1]

@then(u'we get the fib number 55')
def step_impl(context):
    context.expected_number = 55
    assert context.fib_number == context.expected_number, "Calc fib number: %d" % context.fib_number
```
- 實作出 `fibs`
- 修改每個 `step_impl`

> `list(fibs(context.fib_number))[-1]`: 將 `fibs()` 計算結果轉成 `list`，然侯取出最後一個值 (寫得很有技巧，但可讀性很差)

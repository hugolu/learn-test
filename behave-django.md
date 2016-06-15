# behave-django

## 安裝

behave-django 要安裝在 Django project 中，在這之前要先設定虛擬環境、安裝 Django、產生 Django project

```shell
$ source venv/bin/activate
$ pip install Django==1.9.7
$ django-admin.py startproject blog
$ cd blog/
$ pip install behave-django
```

修改 blog/settings.py，新增 behave_django app
```python
INSTALLED_APPS = [
    ...
    'behave_django',
]
```

### 一個簡單的範例

產生以下目錄與檔案
```
features/
├── environment.py
├── running-tests.feature
└── steps
    └── running_tests.py
```

features/environment.py:
```python
"""
behave environment module for testing behave-django
"""

def before_feature(context, feature):
    if feature.name == 'Fixture loading':
        context.fixtures = ['behave-fixtures.json']


def before_scenario(context, scenario):
    if scenario.name == 'Load fixtures for this scenario and feature':
        context.fixtures.append('behave-second-fixture.json')
```

features/running-tests.feature:
```python
"""
behave environment module for testing behave-django
"""

def before_feature(context, feature):
    if feature.name == 'Fixture loading':
        context.fixtures = ['behave-fixtures.json']

def before_scenario(context, scenario):
    if scenario.name == 'Load fixtures for this scenario and feature':
        context.fixtures.append('behave-second-fixture.json')
(venv) vagrant@debian:~/myWorkspace/blog$ cat features/running-tests.feature
Feature: Running tests
    In order to prove that behave-django works
    As the Maintainer
    I want to test running behave against this features directory

    Scenario: The Test
        Given this step exists
        When I run "python manage.py behave"
        Then I should see the behave tests run
```

features/steps/running_tests.py:
```python
from behave import given, when, then

@given(u'this step exists')
def step_exists(context):
    pass

@when(u'I run "python manage.py behave"')
def run_command(context):
    pass

@then(u'I should see the behave tests run')
def is_running(context):
    pass
```

執行測試
```shell
$ python manage.py behave

Creating test database for alias 'default'...
Feature: Running tests # features/running-tests.feature:1
  In order to prove that behave-django works
  As the Maintainer
  I want to test running behave against this features directory
  Scenario: The Test                       # features/running-tests.feature:6
    Given this step exists                 # features/steps/running_tests.py:4 0.000s
    When I run "python manage.py behave"   # features/steps/running_tests.py:9 0.000s
    Then I should see the behave tests run # features/steps/running_tests.py:14 0.000s

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
3 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m0.000s
Destroying test database for alias 'default'...
```

> 附註：從 0.2.0 開始，不再需要在 environment.py 中插入 `environment.before_scenario()` 與 `environment.after_scenario()`。

-= TBC =-
----
## 參考

- https://pythonhosted.org/behave-django/index.html (文件)
- https://github.com/behave/behave-django/tree/master/features (範例)

# behave-django

## 安裝

behave-django 要安裝在 Django project 中，在這之前要先設定虛擬環境、安裝 Django、產生 Django project

```shell
$ source venv/bin/activate
$ pip install Django==1.9.7
$ django-admin.py startproject mysite
$ cd mysite/
$ pip install behave-django
```

修改 mysite/settings.py，新增 behave_django app
```python
INSTALLED_APPS = [
    ...
    'behave_django',
]
```

### 一個簡單的範例

在 mysite/ 目錄裡產生以下目錄與檔案
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

### 下載範例

```shell
$ git clone https://github.com/behave/behave-django
```

以下，透過下載範例進行說明。

## 用法

### 網頁瀏覽器自動化 (Web browser automation)

網頁自動化函式庫可以透過 `context.base_url` 存取伺服器。此外，使用 `context.get_url()` 得到保留專案URL與絕對路徑。

```python
# Get context.base_url
context.get_url()

# Get context.base_url + '/absolute/url/here'
context.get_url('/absolute/url/here')

# Get context.base_url + reverse('view-name')
context.get_url('view-name')

# Get context.base_url + reverse('view-name', 'with args', and='kwargs')
context.get_url('view-name', 'with args', and='kwargs')

# Get context.base_url + model_instance.get_absolute_url()
context.get_url(model_instance)
```

#### 網頁自動化測試

透過瀏覽器打開 `http://192.168.33.10:8000/`，得到下面內容
```
Behave Django works
```

以下驗證透過瀏覽器看到的內容合乎預期。

features/live-test-server.feature
```
Feature: Live server
    In order to prove that the live server works
    As the Maintainer
    I want to send an HTTP request

    Scenario: HTTP GET
        When I visit "/"
        Then I should see "Behave Django works"
```

features/steps/live_test_server.py
```python
@when(u'I visit "{url}"')
def visit(context, url):
    page = urlopen(context.base_url + url)
    context.response = str(page.read())

@then(u'I should see "{text}"')
def i_should_see(context, text):
    assert text in context.response
```
- 透過 `context.base_url` 取得網頁URL，使用 `urlopen()` 取得網頁物件
- `context.response = str(page.read())` 讀取網頁內容
- `assert text in context.response` 驗證讀取的網頁內容符合預期

執行結果
```shell
$ python manage.py behave --include=live-test-server
Creating test database for alias 'default'...
Feature: Live server # features/live-test-server.feature:1
  In order to prove that the live server works
  As the Maintainer
  I want to send an HTTP request
  Scenario: HTTP GET                        # features/live-test-server.feature:6
    When I visit "/"                        # features/steps/live_test_server.py:9 0.008s
    Then I should see "Behave Django works" # features/steps/live_test_server.py:15 0.000s

1 feature passed, 0 failed, 0 skipped
1 scenario passed, 0 failed, 0 skipped
2 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m0.009s
Destroying test database for alias 'default'...
```

### 測試用客戶端 (Django’s testing client)

`context` 包含 TestCase 的實例。`context.test` 提供 Django 測試客戶端程式，驗證透過 URL 讀取網頁內容是否合乎預期。

修改 features/steps/live_test_server.py
```python
@when(u'I visit "{url}"')
def visit(context, url):
    context.response = context.test.client.get(url)

@then(u'I should see "{text}"')
def i_should_see(context, text):
    context.test.assertContains(context.response, text)
```
- `context.text` 提供一堆類似 unittest 的函式，例如 `assertRedirects`, `assertContains`, `assertNotContains`, `assertFormError`, `assertFormsetError`, `assertTemplateUsed`, `assertTemplateNotUsed`, `assertRaisesMessage`, `assertFieldOutput`, `assertHTMLEqual`, `assertHTMLNotEqual`, `assertInHTML`, `assertJSONEqual`, `assertJSONNotEqual`, `assertXMLEqual`, `assertXMLNotEqual`, `assertQuerysetEqual`, `assertNumQueries`

### 資料庫事務 (Database transactions per scenario)

----
## 參考

- https://pythonhosted.org/behave-django/index.html (文件)
- https://github.com/behave/behave-django/tree/master/features (範例)

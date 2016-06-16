# 實驗

## BDD

目標：**溝通**帳號註冊與登入的邏輯

先產生專案目錄，再建立 features 與 steps 目錄
```shell
$ mkdir bdd
$ cd bdd
$ mkdir -p features/steps
$ tree
.
└── features
    └── steps
```

### 描述功能 (Feature)

在 features/account.feature 檔案一開頭，使用文字描述功能特性，讓創建規格的**產品經理**與實作功能的**工程師**在相同的 context 下進行溝通。
```
Feature: User account
    In order to buy or sell commodities
    As a buyer or seller
    I want to have a account in the web site
```

### 登入邏輯

在 features/account.feature 描述帳號登入的場景
```
    Scenario: Login as correct username and password
        Given an username "django" with the password "django123" is registered
         When I login as "django" and give the password "django123"
         Then I get the login result: "successful"
    
    Scenario: Login as incorrect username and password
        Given an username "django" with the password "django123" is registered
         When I login as "django" and give the password "abcdef123"
         Then I get the login result: "failed"
```

在什麼事情都沒做的情形下，先看看執行 behave 會發生什麼
```shell
$ behave
...(略)
Failing scenarios:
  features/account.feature:6  Login as correct username and password
  features/account.feature:11  Login as incorrect username and password

0 features passed, 1 failed, 0 skipped
0 scenarios passed, 2 failed, 0 skipped
0 steps passed, 0 failed, 0 skipped, 6 undefined
Took 0m0.000s

You can implement step definitions for undefined steps with these snippets:

@given(u'an username "django" with the password "django123" is registered')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given an username "django" with the password "django123" is registered')

@when(u'I login as "django" and give the password "django123"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I login as "django" and give the password "django123"')

@then(u'I get the login result: "successful"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I get the login result: "successful"')

@when(u'I login as "django" and give the password "abcdef123"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I login as "django" and give the password "abcdef123"')

@then(u'I get the login result: "failed"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I get the login result: "failed"')
```
- 沒有實作 steps，得到兩個 Failing scenarios
- behave 很貼心的幫我們產生一些 snippet

接下用這些 snippet 產生 features/steps/account.py (暫時把 raise 改成 pass，假裝我們已經把真正的功能實作出來)
```python
@given(u'an username "django" with the password "django123" is registered')
def step_impl(context):
    pass

@when(u'I login as "django" and give the password "django123"')
def step_impl(context):
    pass

@then(u'I get the login result: "successful"')
def step_impl(context):
    pass

@when(u'I login as "django" and give the password "abcdef123"')
def step_impl(context):
    pass

@then(u'I get the login result: "failed"')
def step_impl(context):
    pass
```

在執行 behave 得到下面結果
```shell
$ behave
Feature: User account # features/account.feature:1
  In order to buy or sell commodities
  As a buyer or seller
  I want to have a account in the web site
  Scenario: Login as correct username and password                         # features/account.feature:6
    Given an username "django" with the password "django123" is registered # features/steps/account.py:1 0.000s
    When I login as "django" and give the password "django123"             # features/steps/account.py:5 0.000s
    Then I get the login result: "successful"                              # features/steps/account.py:9 0.000s

  Scenario: Login as incorrect username and password                       # features/account.feature:11
    Given an username "django" with the password "django123" is registered # features/steps/account.py:1 0.000s
    When I login as "django" and give the password "abcdef123"             # features/steps/account.py:13 0.000s
    Then I get the login result: "failed"                                  # features/steps/account.py:17 0.000s

1 feature passed, 0 failed, 0 skipped
2 scenarios passed, 0 failed, 0 skipped
6 steps passed, 0 failed, 0 skipped, 0 undefined
Took 0m0.001s
```
- 測試一個 feature，其中包含兩個 scenario、六個 step
- 測試通過

### 註冊邏輯

在 features/account.feature 描述帳號登入的場景，這次使用 `Scenario Outline` 描述多個測試場景
```
    Scenario Outline: username and password must be large than 5 characters
         When try to register a name <username> with a password <password>
         Then I get the register result: <result>

        Examples: some usernames and passwords
            | username  | password  | result                            |
            | abc       | 123456    | "username or password too short"  |
            | abcedf    | 123       | "username or password too short"  |
            | abc       | 123       | "username or password too short"  |
            | abcdef    | 123456    | "the account is created"          |
```

在 features/steps/account.py 中，相對應的步驟如下
```python
@when(u'try to register a name {username} with a password {password}')
def step_impl(context, username, password):
    pass

@then(u'I get the register result: "username or password too short"')
def step_impl(context):
    pass

@then(u'I get the register result: "the account is created"')
def step_impl(context):
    pass
```
- 使用 `{username}`, `{password}`, `{result}` 

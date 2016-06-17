from account import *

@given(u'< 帳號{username}與密碼{password}已註冊')
def step_impl(context, username, password):
    account_insert(username, password)

@when(u'< 我用{username}與密碼{password}登入')
def step_impl(context, username, password):
    if account_login(username, password) == True:
        context.result = "成功"
    else:
        context.result = "失敗"

@then(u'< 我得到登入結果：{result}')
def step_impl(context, result):
    assert(context.result == result)

@when(u'< 嘗試用帳號{username}與密碼{password}註冊')
def step_impl(context, username, password):
    if account_register(username, password) == True:
        context.result = "帳號建立"
    else:
        context.result = "無效的帳號或密碼"

@then(u'< 我得到註冊結果：{result}')
def step_impl(context, result):
    assert(context.result == result)

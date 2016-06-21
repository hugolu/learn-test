from account.models import Account

@given(u'< 帳號{username}與密碼{password}被註冊')
def step_impl(context, username, password):
    Account.objects.create(username=username, password=password)

@when(u'< 我用帳號{username}與密碼{password}登入')
def step_impl(context, username, password):
    context.result = "成功" if Account.objects.verify(username, password) else "失敗"

@then(u'< 我得到登入結果：{result}')
def step_impl(context, result):
    assert(context.result == result)

@when(u'< 嘗試用帳號{username}與密碼{password}註冊')
def step_impl(context, username, password):
    context.result = "成功" if Account.objects.register(username, password) else "無效的帳號或密碼"

@then(u'< 我得到註冊結果：{result}')
def step_impl(context, result):
    assert(context.result == result)

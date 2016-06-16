@given(u'< 帳號"django"與密碼"django123"被註冊')
def step_impl(context):
    pass

@when(u'< 我用"django"與密碼"django123"登入')
def step_impl(context):
    pass

@then(u'< 我得到註冊結果"成功"')
def step_impl(context):
    pass

@when(u'< 我用"django"與密碼"abcdef123"登入')
def step_impl(context):
    pass

@then(u'< 我得到註冊結果"失敗"')
def step_impl(context):
    pass

@then(u'< 我得到登入結果"成功"')
def step_impl(context):
    pass

@then(u'< 我得到登入結果"失敗"')
def step_impl(context):
    pass

@when(u'< 嘗試用帳號{username}與密碼{password}註冊')
def step_impl(context, username, password):
    pass

@then(u'< 我得到註冊結果{result}')
def step_impl(context, result):
    pass

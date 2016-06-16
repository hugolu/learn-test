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

@when(u'try to register a name {username} with a password {password}')
def step_impl(context, username, password):
    pass

@then(u'I get the register result: {result}')
def step_impl(context, result):
    pass

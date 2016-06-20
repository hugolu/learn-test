from account.models import Account

@given(u'an username {username} with the password {password} is registered')
def step_impl(context, username, password):
    Account.objects.create(username=username, password=password)

@when(u'I login as {username} and give the password {password}')
def step_impl(context, username, password):
    context.result = "successful" if Account.objects.login(username, password) else "failed"

@then(u'I get the login result: {result}')
def step_impl(context, result):
    assert(context.result == result)

@when(u'try to register a name {username} with a password {password}')
def step_impl(context, username, password):
    context.result = "successful" if Account.objects.register(username, password) else "invalid username or password"

@then(u'I get the register result: {result}')
def step_impl(context, result):
    assert(context.result == result)

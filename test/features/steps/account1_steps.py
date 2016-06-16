from account import *

@given(u'an username {username} with the password {password} is registered')
def step_impl(context, username, password):
    account_insert(username, password)

@when(u'I login as {username} and give the password {password}')
def step_impl(context, username, password):
    if account_login(username, password) == True:
        context.result = "successful"
    else:
        context.result = "failed"

@then(u'I get the login result: {result}')
def step_impl(context, result):
    assert(context.result == result)

@when(u'try to register a name {username} with a password {password}')
def step_impl(context, username, password):
    if account_register(username, password) == True:
        context.result = "successful"
    else:
        context.result = "invalid username or password"

@then(u'I get the register result: {result}')
def step_impl(context, result):
    assert(context.result == result)

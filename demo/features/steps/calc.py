from calc.calculator import Calculator

@given(u'I enter {expr}')
def step_impl(context, expr):
    context.expr = expr

@when(u'I press "=" button')
def step_impl(context):
    calc = Calculator()
    context.answer = calc.evalString(context.expr)

@then(u'I get the answer {answer}')
def step_impl(context, answer):
    try:
        ans = float(answer)
    except ValueError:
        ans = answer

    assert context.answer == ans

@when(u'I enter {expr1} first')
def step_impl(context, expr1):
    calc = Calculator()
    context.answer1 = calc.evalString(expr1)

@when(u'I enter {expr2} again')
def step_impl(context, expr2):
    calc = Calculator()
    context.answer2 = calc.evalString(expr2)

@then(u'I get the same answer')
def step_impl(context):
    assert context.answer1 == context.answer2

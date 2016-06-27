from calc.calculator import Calculator

@given(u'< 我輸入{expr}')
def step_impl(context, expr):
    context.expr = expr

@when(u'< 我按下等號按鈕')
def step_impl(context):
    calc = Calculator()
    context.answer = calc.evalString(context.expr)

@then(u'< 我得到的答案是{answer}')
def step_impl(context, answer):
    try:
        ans = float(answer)
    except ValueError:
        ans = answer

    assert context.answer == ans

@when(u'< 我先輸入{expr1}')
def step_impl(context, expr1):
    calc = Calculator()
    context.answer1 = calc.evalString(expr1)

@when(u'< 我再輸入{expr2}')
def step_impl(context, expr2):
    calc = Calculator()
    context.answer2 = calc.evalString(expr2)

@then(u'< 我得到相同的答案')
def step_impl(context):
    assert context.answer1 == context.answer2

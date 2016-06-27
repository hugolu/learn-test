from django.shortcuts import render
from django.http import HttpResponse
from .calculator import Calculator


# Create your views here.
def calc(request):
    value = ''
    if request.method == 'POST':
        calc = Calculator()
        expr = request.POST['expr']
        value = calc.evalString(expr)
    return render(request, 'calculator.html', {'value': value})

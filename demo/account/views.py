from django.shortcuts import render
from account.models import Account
from django import forms
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
def home(request):
    return HttpResponse('hello world')

class LoginForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'password', ]

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            if Account.objects.login(a.username, a.password):
                return HttpResponseRedirect('/')

    form = LoginForm()
    return render(request, 'login.html', {'form': form})

class RegisterForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'password']

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            a = form.save(commit=False)
            if Account.objects.register(a.username, a.password):
                return HttpResponseRedirect('/login')

    form = RegisterForm()
    return render(request, 'register.html', {'form': form})

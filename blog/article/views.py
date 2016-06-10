from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from article.models import Article
from django import forms

# Create your views here.
def home(request):
    s = "Hello World!"
    return HttpResponse(s)

def detail(request, pk):
    article = Article.objects.get(pk=int(pk))
    return render(request, 'detail.html', {'article': article})

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', ]

def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_article = form.save()
            return HttpResponseRedirect('/article/' + str(new_article.pk))

    form = ArticleForm()
    return render(request, 'create_article.html', {'form': form}) 

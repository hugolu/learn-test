# Django

雖然 Django 跟 BDD/TDD 沒有直接的關係，但為了開發流程的完整概念，我嘗試把 Django 這個 web framework 安裝起來，然後在上面開發與測試。

練習過程以這份 [Django Tutorial](http://daikeren.github.io/django_tutorial/) 為主，但因為版本關係有些使用方式太舊，參考了另一份 [Django Girls 學習指南](https://www.gitbook.com/book/djangogirlstaipei/django-girls-taipei-tutorial/details) 作為輔助。

> 本來想練習 Django 官網提供的土托魚 Writing your first Django app, part [1](https://docs.djangoproject.com/en/1.9/intro/tutorial01/), [2](https://docs.djangoproject.com/en/1.9/intro/tutorial02/), [3](https://docs.djangoproject.com/en/1.9/intro/tutorial03/), [4](https://docs.djangoproject.com/en/1.9/intro/tutorial04/), [5](https://docs.djangoproject.com/en/1.9/intro/tutorial05/), [6](https://docs.djangoproject.com/en/1.9/intro/tutorial06/), [7](https://docs.djangoproject.com/en/1.9/intro/tutorial07/)，但這一系列鉅細彌遺的讓人有點吃不消 (我只想快速上手啊，摔筆)，只好改看其他人消化吸收過的東西。

Let's 開始練功吧！

## 簡介

世界上除了 RoR 之外，還有其他 Web Framework，像是 Node.js 以及 Django。

如同 Python 生態環境之豐富，Django 也有很多如資料庫、表單、登入系統、管理界面等元件，大大縮短了後端開發的時間。

## 安裝 Django

安裝與管理套件版本是軟體開發頗讓人頭疼的一環，幸好靠著  pyenv 管理多個 Python 版本問題，與 virtualenv 創造虛擬（獨立）Python 環境的工具，Python 工程師的生活才能過得輕鬆點。

安裝 pyenv 與 virtualenv
```shell
$ git clone https://github.com/yyuu/pyenv.git ~/.pyenv
$ git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
$ sudo pip install virtualenv
```

設定 ~/.bashrc
```
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

重新載入 ~/.bashrc
```shell
$ source ~/.bashrc
```

安裝 Python 3.5.1
```shell
$ pyenv install 3.5.1
```

設定 Python 3.5.1
```shell
$ pyenv local 3.5.1
$ python --version
Python 3.5.1
```

設定虛擬環境 (從此只要在 virtualenv 下面安裝的 package 都只會存在于這個 virtualenv 當中，安裝套件不需要 root 權限)
```shell
$ pyvenv myvenv
$ source myvenv/bin/activate
(myvenv) vagrant@debian:~$
```

下載、安裝 Django
```shell
$ pip install Django==1.9.7
```

## Djando Project

建立 project
```shell
$ django-admin.py startproject blog
$ tree blog/
blog/
├── blog
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```
- 內層的 `blog/` 放置 project 相關的設定

進入 `blog/` 啟動服務
```shell
$ cd blog/
$ python manage.py runserver 0.0.0.0:8000
```

開啟瀏覽器，連接 `http://192.168.33.10:8000/` ([虛擬機](environment.md))，看到以下訊息
```
It worked!
Congratulations on your first Django-powered page.
```

## Django APPs

- Django Project 由多個 Django APP 組成，每個 Django App 可以被多個 Django Project 所使用
- Django App 就是一個功能單純的應用

創建 Django App
```shell
$ python manage.py startapp article
$ tree article/
article/
├── admin.py
├── apps.py
├── __init__.py
├── migrations
│   └── __init__.py
├── models.py
├── tests.py
└── views.py
```

讓 project 知道多了這個 app，編輯 `blog/settings.py`
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'article',
]
```
- 在 INSTALLED_APPS 內新增 `article`

## Django Views & Django URLs

Django 不採取 MVC 架構，而是 MTV 架構。操作 View 與 URL 之前，先由下圖了解 URL Request 被如何處理，然後變成使用者在瀏覽器看到的結果。

![Python MTV model](http://1.bp.blogspot.com/-zsIAtTJ0aNg/VdgZlmmnADI/AAAAAAAA6A0/edFRO2N9Yb8/s1600/432038560_9f8b830dfe_o.png)(圖片出處 http://mropengate.blogspot.tw/2015/08/mvcdjangomtv.html)

1. URL 派送器 (urls.py) 將 URL Request 對應到 View 的函式
2. View 函式 (views.py) 執行 request 動作，通常引發讀寫資料庫的動作
3. Model (models.py) 定義資料庫的資料以及如何跟它互動的方式
4. 處理完 request 任務，View 就會回覆 HTTP Response 給瀏覽器
5. Templates 放置 HTML 檔案，這些檔案包含 HTML 語法與網頁如何呈現的邏輯

創建一個 View，修改 article/views.py，新增一下程式
```python
from django.http import HttpResponse

def home(request):
    s = "Hello World!"
    return HttpResponse(s)
```
- 沒有涉及底層 Model，僅僅回覆 "Hello World!" 訊息

告訴 Django 要如何處理 URL，修改 blog/urls.py，在 `urlpatterns` 加入下面程式
```python
urlpatterns = [
    ...
    url(r'^$', 'article.views.home'),
]
```

重啟服務，連接 `http://192.168.33.10:8000/`，看到以下訊息
```
Hello World!
```

## Django Model

Django 支援許多資料庫，只要簡單設定就能存取 sqlite、PostgreSQL、MySQL 與 Oracle。

與資料庫相關設定放在 blog/settings.py，來看看
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
- `ENGINE` 採用 sqlite3
- `NAME` 宣告資料庫檔案位置在 `blog/db.sqlite3`

Django 中透過 Model 來處理與底層資料庫的互動，要在 Model 定義表格的存取方式

- Model 繼承 `django.db.models.Model`
- Model 的屬性 (attribute) 都是一個資料庫的欄位
- 透過 Model API 執行資料庫 query，將每種資料庫 SQL 版本間的差異隱藏起來

設定 blog/article 的資料 Model，修改 articles/models.py，加入以下程式碼
```python
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(u'Name', max_length=50)

    def __str__(self):
        return self.name

class Article(models.Model):
    content = models.TextField(u'Content')
    title = models.CharField(u'Title', max_length=50)
    category = models.ForeignKey('Category', blank=True, null=True)

    def __str__(self):
        return self.title
```
- 建立兩個 Model: Category & Article
- Category 宣告一個屬性: `name`，並定義 `__str__` 用字串表示自己
- Article 宣告三個屬性: `content` 表示文章內容, `title` 表示文章標題, `category` 使用 `ForeignKey` 定義資料表格間的關聯性

剛剛只是定義 Model，資料庫的表格還沒建立起來，要透過以下指令產生
```shell
$ python manage.py makemigrations
$ python manage.py migrate
```

現在透過 Django 提供的 shell 來看看資料庫表格的樣子
```
$ python manage.py shell
>>> 
```
- 看到 `>>>` 提示符號表示進入 Python REPL

試試創建三筆記錄
```python
>>> from article.models import Article, Category
>>> Article.objects.create(content="Test1", title="article 1")
<Article: article 1>
>>> Article.objects.create(content="Test2", title="article 2")
<Article: article 2>
>>> c = Category.objects.create(name="category 1")
>>> Article.objects.create(content="Test3", title="article 3", category=c)
<Article: article 3>
>>>
```

查詢剛剛插入的資料
```python
>>> Article.objects.all()
[<Article: article 1>, <Article: article 1>, <Article: article 2>, <Article: article 3>]
>>> for article in Article.objects.all():
...     print(article.title)
...
article 1
article 2
article 3
```

修改一筆記錄
```python
>>> from article.models import Article, Category
>>> a = Article.objects.get(title="article 1")
>>> a.title = "Article"
>>> a.save()
```

操作完畢，使用 Ctrl-D 離開 Python REPL

Django Model 幫忙處理了與資料庫互動的部分，我很好奇它做了什麼，以下透過 sqlite 直接下 SQL 來看看
```shell
$ sqlite3 db.sqlite3
```

透過 `.table` 命令列出所有表格
```mysql
sqlite> .tables
article_article             auth_user_groups
article_category            auth_user_user_permissions
auth_group                  django_admin_log
auth_group_permissions      django_content_type
auth_permission             django_migrations
auth_user                   django_session
```
- `article_article` 對應到 article/models.py 裡面的 `class Article(models.Model)`
- `article_category` 對應到 article/models.py 裡面的 `class Category(models.Model)`

使用 `.schema` 顯示表格 schema
```sql
sqlite> .schema article_article
CREATE TABLE "article_article" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "content" text NOT NULL, "title" varchar(50) NOT NULL, "category_id" integer NULL REFERENCES "article_category" ("id"));
CREATE INDEX "article_article_b583a629" ON "article_article" ("category_id");
sqlite> .schema article_category
CREATE TABLE "article_category" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "name" varchar(50) NOT NULL);
```
- 除了原先設定的表格，Django Model 還透過 `id` 維護一個自動增加的唯一主鍵

查詢 `article_article` 與 `article_category` 表格內容
```sql
sqlite> .header on
sqlite> .mode column
sqlite> SELECT * FROM article_article;
id          content     title       category_id
----------  ----------  ----------  -----------
1           Test1       Article
2           Test2       article 2
3           Test3       article 3   1
sqlite> SELECT * FROM article_category;
id          name
----------  ----------
1           category 1
```

不做任何修改，使用 `.quit` 離開
```sql
sqlite> .quit
```

## Django Admin

除了可以透過 Shell 操作 Model，Django 提供了 admin app 讓使用者可以透過 web UI 做創造、讀取、更新、刪除的動作。

Django 預設安裝 admin，打開 blog/settings.py 查看
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    ...
]
```

URL 導向設定在 blog/urls.py
```python
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    ...
]
```

修改 article/admin.py，告訴 Django 建立了 Category, Article 這兩個 Model
```python
from django.contrib import admin
from article.models import Article, Category

# Register your models here.
admin.site.register(Article)
admin.site.register(Category)
```

設定 superuser 帳號
```shell
$ python manage.py createsuperuser
Username (leave blank to use 'vagrant'): django
Email address: printk@gmail.com
Password:
Password (again):
Superuser created successfully.
You have mail in /var/mail/vagrant
```

設定完成，啟動服務，登入 http://192.168.33.10:8000/admin/，透過 Web UI 新增、查詢、修改、刪除記錄。

## Django Views & Django URL 再訪

想辦法做出讓網站可以根據 URL 動態產生網頁，例如 URL=`article/1/` 呈顯第一則文章

先從 view 開始，修改 article/views.py，加上下面程式碼
```python
from article.models import Article

def detail(request, pk):
    article = Article.objects.get(pk=int(pk))
    s = """
    <html>
    <head></head>
    <body>
    <h1>{0}</h1>
    {1}
    </body>
    </html>
    """.format(article.title, article.content)
    return HttpResponse(s)
```
- `detail` 根據參數 `pk` 查詢文章的標題與內容，插入 HTML 中，然後回覆給瀏覽器

接著，修該 blog/urls.py，讓 Django 能夠解析 URL Request，得到要給 `detail` 的 `pk`
```python
urlpatterns = [
    ...
    url(r'^article/(?P<pk>[0-9]+)/$', 'article.views.detail'),
]
```
- `(?P<pk>[0-9]+)` 解析 URL=`article/1` 後面的數字，得到 pk 這個 group name 然後傳給 `detail`
- [Named Group](https://docs.djangoproject.com/ja/1.9/topics/http/urls/#named-groups): In Python regular expressions, the syntax for named regular-expression groups is `(?P<name>pattern)`, where `name` is the name of the group and `pattern` is some pattern to match.

設定完成，啟動服務，打開 http://192.168.33.10:8000/article/1 ，看到第一篇文章的標題與內容。
```
Article

Test1
```

## Django Template

剛剛把 HTML 放在 View 會讓邏輯控制與網頁呈現的程式碼交錯混合，增加了前後端工程的複雜度。接下來要將 HTML 的提到 Templates 目錄中，讓前端網頁設計師處理 HTML 時不需要知道後端操作的邏輯。

在 article 目錄創建 templates 目錄，裡面新增一個檔案 article/templates/detail.html
```html
<html>
<head></head>
<body>
<h1>{{ article.title }}</h1>
{{ article.content }}
</body>
</html>
```
- Django 定義許多 [template languate](https://docs.djangoproject.com/en/1.9/ref/templates/language/)，方便前端工程師存取後端的變數
- 這個 HTML 預期被 View 呼叫時會得到 `article` 物件，藉由 `{{ article.title }}` 與 `{{ article.content }}` 取得文章的標題與內容

修改之前的 View，article/views.py
```python
def detail(request, pk):
    article = Article.objects.get(pk=int(pk))
    return render(request, 'detail.html', {'article': article})
```
- 透過 python dictionary 傳遞 `article` 變數給 template

除了簡單的變數取代，還可以使用 [if](https://docs.djangoproject.com/en/1.9/ref/templates/builtins/#std:templatetag-if) tag 與 [up](https://docs.djangoproject.com/en/1.9/ref/templates/builtins/#upper) filter 增加 template 的變化。修改 article/templates/detail.html
```html
<html>
<head></head>
<body>
<h1>{{ article.title }}</h1>
{% if article.pk == 1 %}
{{ article.content|upper }}
{% else %}
{{ article.content }}
{% endif %}
</body>
</html>
```

設定完成，啟動服務，打開 http://192.168.33.10:8000/article/1 ，看到第一篇文章的內容是否變成大寫。
```
Article

TEST1
```

## Django Forms

除了透過 Django Admin 修改資料，還可以手動產生自己的介面。

傳統 framework 會這麼做:

- 用 HTML 刻個 form
- 處理 HTTP POST request
- 檢查表單欄位內容是否正確
- 把確認過的資料存進 database 當中

Django Form 提供另一種方便的方式，產生表單對應相對 Model 欄位，提供讀取、修改的功能。

先在 article/views.py 產生一個表單類別
```python
from django import forms

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', ]
```

然後告訴 View 如何處理 ArticleForm
```python
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            new_article = form.save()
            return HttpResponseRedirect('/article/' + str(new_article.pk))

    form = ArticleForm()
    return render(request, 'create_article.html', {'form': form})
```
- 如果 request 是 POST，表示使用者送出表單，則驗證資料合法後寫入資料庫，然後將網頁導向剛剛輸入的資料
- 如果 request 不是 POST，表示使用者準備填寫表單，則送出 `create_article.html`

接者產生 article/templates/create_article.html，讓使用者可以填寫資料
```html
<html>
<head></head>
<body>
<form action="." method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <input type="submit" />
</form>
</body>
</html>
```
- 透過 `form.as_p` 在 HTML 中產生表單
- 使用 `csrf_token` 做到 [Cross Site Request Forgery protection](https://docs.djangoproject.com/en/dev/ref/contrib/csrf/)，避免網站被攻擊

> [[技術分享] Cross-site Request Forgery (Part 1)](http://cyrilwang.pixnet.net/blog/post/31813568-%5B%E6%8A%80%E8%A1%93%E5%88%86%E4%BA%AB%5D-cross-site-request-forgery-(part-1)): 簡單來說，CSRF 就是在使用者不知情的情況下，讓瀏覽器送出請求給目標網站以達攻擊目的。 對於 HTTP 協定有所了解的讀者，看到這句話可能會覺得很困惑。因為在預設的情況下，任何人只要知道 URL 與參數都可以對網站發出任何請求，如此說來不是所有的網站都會遭受 CSRF 的攻擊了嗎？可以說是，也可以說不是。因此嚴格來說，CSRF 通常指的是發生在使用者已經登入目標網站後，駭客利用受害者的身分來進行請求，如此一來不但可以獲得受害者的權限，而且在系統的相關紀錄中也很難發現可疑之處。

最後修改 blog/urls.py，把 URL request 與 View 串起來
```python
urlpatterns = [
    ...
    url(r'^create/$', 'article.views.create'),
]
```

設定完成，啟動服務，打開 http://192.168.33.10:8000/create 產生一篇文章，送出表單看看是否被導向剛剛產生的文章。
```
hello world

this is a test
```

## Django 的第三方套件們

除了 Django 自帶的套件，[Django Packages](https://www.djangopackages.com/) 提供更多樣化的套件。

接下來試著安裝 django-grappelli，讓 admin 畫面變得更漂亮些。

安裝套件
```shell
$ pip install django-grappelli
```

告訴 Django 新增 app，修改 blog/settings.py
```python
INSTALLED_APPS = [
    'grappelli',
    'django.contrib.admin',
    ...
]
```
- 加入 grappelli 放在 django.contrib.admin 之前

修改 blog/urls.py，加上相對 URL
```python
from django.conf.urls import include

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),
    ...
]
```
> 實驗發現，似乎不需要修改 blog/urls.py 這部分，只要在 blog/settings.py 新增 'grappelli' 這個 app 即可

設定完成，啟動服務，打開 http://192.168.33.10:8000/admin 看看網頁是不是變漂亮了。

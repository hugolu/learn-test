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

## Deploy 前置動作

目前所做的工作只能透過本機瀏覽器看到結果，想讓全世界看到你的作品就要部署到伺服器上。[Heroku](https://dashboard.heroku.com/) 提供免費額度的服務給一些小型網站，讓還沒獲利的網站可以免費營運。接下來設定部署環境準備將剛剛寫的程式放上雲端。

安裝部署需要的工具
```shell
$ pip install dj-database-url gunicorn dj-static
```

將虛擬環境套件的版本列出來，儲存在 requirements.txt
```shell
$ pip freeze > requirements.txt
```

建立 Procfile 檔案，告訴 Heroku 要如何啟動我們的應用
```
web: gunicorn --pythonpath blog blog.wsgi
```

為了讓 Heroku 知道要用哪一個版本的 Python，新增 runtime.txt 
```
python-3.5.1
```

跟 blog/settings.py 不同，正式上線的環境透過 blog/production_settings.py 來設定
```python
# Import all default settings.
from .settings import *

import dj_database_url
DATABASES = {
    'default': dj_database_url.config()
}

# Static asset configuration.
STATIC_ROOT = 'staticfiles'

# Honor the 'X-Forwarded-Proto' header for request.is_secure().
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers.
ALLOWED_HOSTS = ['*']

# Turn off DEBUG mode.
DEBUG = False
```

WSGI - Web Server Gateway Interface 是 Python 定義網頁程式和伺服器溝通的介面。為了讓 Heroku 的服務能夠透過 WSGI 介面與我們的網站溝通，修改 blog/wsgi.py 如下：
```python
import os
from django.core.wsgi import get_wsgi_application
from dj_static import Cling

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
application = Cling(get_wsgi_application())
```
- 將 dj_static 引入，並在 application 上使用它，以協助幫我們部署 static 檔案（例如圖片、CSS、JavaScript 檔案等等）

不想把開發時使用的檔案，例如虛擬環境、本機資料庫、Python cache等等放到網路上。建立一個 .gitignore 檔案，排除這些資料
```
*.pyc
__pycache__
staticfiles
db.sqlite3
```

## Deploy to Heroku

在開始部署（deploy）之前

1. 註冊 Heroku 帳號：https://id.heroku.com/signup
2. 安裝 Heroku 工具箱：https://toolbelt.heroku.com

以虛擬機 (ARTACK/debian-jessie) 為例，安裝工具步驟如下
```shell
$ wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh
```

### Step 1. 登入 Heroku

```shell
$ heroku login
```

### Step 2. 建立 git repository

```shell
$ git init
$ git add .
$ git commit -m "my blog app"
```

### Step 3-1: 新增新的 Heroku app

新增一個可以上傳 repository 的地方
```shell
$ heroku create
Heroku CLI submits usage information back to Heroku. If you would like to disable this, set `skip_analytics: true` in /home/vagrant/.heroku/config.json
Creating app... done, ⬢ guarded-harbor-11820
https://guarded-harbor-11820.herokuapp.com/ | https://git.heroku.com/guarded-harbor-11820.git
```
- 沒給 app 名稱，由 Heroku 隨機產生，得到 `guarded-harbor-11820`

### Step 3-2: 指定已經存在的 app

用指令 heroku apps 查看新增過 app 的名稱
```shell
$ heroku apps
=== My Apps
guarded-harbor-11820
hidden-brook-77287
```

設定成你想要上傳的 app
```shell
$ heroku git:remote -a guarded-harbor-11820
```

使用 `git remote` 指令檢查剛剛的設定
```shell
$ git remote -v
heroku	https://git.heroku.com/guarded-harbor-11820.git (fetch)
heroku	https://git.heroku.com/guarded-harbor-11820.git (push)
```

### Step 4: 設定環境變數

```shell
$ heroku config:set DJANGO_SETTINGS_MODULE=blog.production_settings
```

### Step 5: 利用 git push 上傳到 Heroku
```shell
$ git push heroku master
Counting objects: 24, done.
Compressing objects: 100% (20/20), done.
Writing objects: 100% (24/24), 5.12 KiB | 0 bytes/s, done.
Total 24 (delta 0), reused 0 (delta 0)
remote: Compressing source files... done.
remote: Building source:
remote:
remote: -----> Python app detected
remote: -----> Installing python-3.5.1
remote:      $ pip install -r requirements.txt
...
```
- python 版本依照 runtime.txt 安裝 python-3.5.1

### Step 6: 啟動 web process

```shell
$ heroku ps:scale web=1
```

### Step 7: Django project 初始化

進行資料庫初始化
```shell
$ heroku run python manage.py migrate
```

為新資料庫建立一個 superuser
```shell
$ heroku run python manage.py createsuperuser
```

### Step 8: 開啟瀏覽器觀看你的網站

透過 open 指令會自動在瀏覽器打開你的網站
```shell
$ heroku open
```

上面那招只能在 terminal console 跟 web browser 在同一個機器的情況下使用，因為我是透過虛擬環境開發的，要自行打開瀏覽器輸入剛剛 heroku 給的 app 名稱加上 “heroku.com” 才能連上，例如 https://guarded-harbor-11820.herokuapp.com/

### Troubleshooting

參考: https://devcenter.heroku.com/articles/application-offline

查看 app 日誌訊息
```shell
$ heroku logs
```

檢查目前 process 狀態
```shell
$ heroku ps
```

顯示應用程式 dyno 使用狀態
```shell
$ heroku scale web=1
Scaling dynos... done, now running web at 1:Free
```

如果掛掉，錯誤訊息會像這樣
```shell
$ heroku ps
=== web (Free): gunicorn --pythonpath blog blog.wsgi (1)
web.1: crashed 2016/06/10 12:00:30 +0200 (~ 17s ago)
```

重新啟動看看能不能解決問題
```shell
$ heroku restart
```

> learn-test/blog 裡面放的就是先前過做的事情，除了 “Deploy to Heroku” 這部分。想將這個 Project 部署到 Heroku，請先複製到 learn-test/ 以外的目錄 (因為 deploy 需要初始化 git repository，這會與 learn-test/.git 衝突)，然後按照 Step1~8 完成部署動作。

## What’s next?

不管是  [Django Tutorial](http://daikeren.github.io/django_tutorial/) 還是 [Django Girls 學習指南](https://www.gitbook.com/book/djangogirlstaipei/django-girls-taipei-tutorial/details) 在文章最後都有一個 Todo list，可能是修改 template 使用 tag/filter 或套用 css/javascript，修改 Model 增加、刪除欄位，上傳檔案，增加留言功能等等。我的下一步是什麼呢？

- 結合 Django 與 Behave，透過與 stakeholder 的對話逐步完成網站的功能
- 使用 Python unittest 開發 View 或 Model 的功能
- 使用 CI 做到測試自動化
- 研究如何自動部署到 Heroku

----
## 參考
-  [Django Tutorial](http://daikeren.github.io/django_tutorial/)
-  [Django Girls 學習指南](https://www.gitbook.com/book/djangogirlstaipei/django-girls-taipei-tutorial/details)
-  [Django documentation](https://docs.djangoproject.com/en/1.9/)

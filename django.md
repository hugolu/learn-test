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

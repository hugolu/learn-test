# Django

雖然 Django 跟 BDD/TDD 沒有直接的關係，但為了開發流程的完整概念，我嘗試把 Django 這個 web framework 安裝起來，然後在上面開發與測試。

Let's 開始練功吧

- [Writing your first Django app, part 1](https://docs.djangoproject.com/en/1.9/intro/tutorial01/)
- [Writing your first Django app, part 2](https://docs.djangoproject.com/en/1.9/intro/tutorial02/)
- [Writing your first Django app, part 3](https://docs.djangoproject.com/en/1.9/intro/tutorial03/)
- [Writing your first Django app, part 4](https://docs.djangoproject.com/en/1.9/intro/tutorial04/)
- [Writing your first Django app, part 5](https://docs.djangoproject.com/en/1.9/intro/tutorial05/)
- [Writing your first Django app, part 6](https://docs.djangoproject.com/en/1.9/intro/tutorial06/)
- [Writing your first Django app, part 7](https://docs.djangoproject.com/en/1.9/intro/tutorial07/)

## 寫出第一支 Django 應用 part 1

### 檢查套件是否安裝
```shell
$ python -c "import django; print(django.get_version())"
1.9.7
```

### 產生目錄

```shell
$ django-admin startproject mysite
$ cd mysite
$ tree
.
├── manage.py
└── mysite
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

1 directory, 5 files
```

###  啟動 Server

```shell
$ python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).

You have unapplied migrations; your app may not work properly until they are applied.
Run 'python manage.py migrate' to apply them.

June 07, 2016 - 08:38:21
Django version 1.9.7, using settings 'mysite.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
- 預設服務綁定 `http://127.0.0.1:8000/`
 
修改服務綁定位置，讓 host os 可以連接
```shell
$ python manage.py runserver 0.0.0.0:8000
```

設定好之後，透過瀏覽器查看結果

![Welcome to Django](welcome2django.png)

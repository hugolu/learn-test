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

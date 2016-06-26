# django-jenkins

## 開始之前

請參考 [django 設定環境](django.md#設定環境)，準備開發環境、建立專案 (假設叫做 demo)...

```shell
$ cd ~/myWorkspace
$ source venv/bin/activate
(venv) vagrant@debian:~/myWorkspace$ cd demo
```
進入 django virtualenv 之後，繼續下面步驟 (以下省略提示符號前文字)

## 安裝 django-jenkins

```shell
pip install django-jenkins
```

## 設定專案

修改 demo/settings.py:
    - 加入 'django_jenkins' App
    - 加入要跑 jenkins test, report 的 App，例如 `calc`

```python
INSTALLED_APPS = [
    'behave_django',
    'django_jenkins',
    ...
    'calc',
]

# Jenkins settings
PROJECT_APPS = [
    'calc',
]

JENKINS_TASKS = (
)
```

## 參考資料

- [django-jenkins](https://github.com/kmmbvnr/django-jenkins) github
- [django-jenkins Tutorial](https://sites.google.com/site/kmmbvnr/home/django-jenkins-tutorial)

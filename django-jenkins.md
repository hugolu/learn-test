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

## 專案版控

初始化 git repository
```shell
$ git init
```

建立 .gitignore，設定哪些檔案不做版本追蹤
```
__pycache__
db.sqlite3
.python-version
*.pyc
.*.swp
reports/
```

上傳 git repository
```shell
$ git add .
$ git commit -m "first commit"
```

## 設定 Jenkins server

開啟瀏覽器，連接 http://192.168.33.10:8000/ ([虛擬機](environment.md))

- Jenkins 管理首頁
    - New Item
        - Item name: `demo`
            - [x] Freestyle project
    - Source Code Management
        - [x] Git
            - Repository URL: `file:///home/vagrant/myWorkspace/demo`
    - Build Triggers
        - [x] Poll SCM
            - Schedule: `* * * * *`
    - Build Environment
        - [x] pyenv build wrapper
            - The Python version: `3.5.1`
    - Build
        - [x] Execute shell
            - Command: [shell command](#shell-command)
    - Post-build Actions
        - [x] Publish Cobertura Coverage Report
            - Cobertura xml report pattern: `reports/coverage.xml`
        - [x] Publish JUnit test result report
            - Test report XMLs: `reports/junit.xml`
        - [x] Report Violations
            - pylint: `reports/pylint.report`
    - Save 

### shell command
```
PATH=$WORKSPACE/venv/bin:/usr/local/bin:$PATH

if [ ! -d "venv" ]; then
        virtualenv venv
fi
. venv/bin/activate
pip install -r requirements.txt

python manage.py jenkins --enable-coverage
```

## 觀看 reports
![Violations report](https://sites.google.com/site/kmmbvnr/home/django-jenkins-tutorial/jenkins-5.png)

![Coverage report](https://sites.google.com/site/kmmbvnr/_/rsrc/1286971838502/home/django-hudson-tutorial/8_coverage_results.png)

![test result](https://sites.google.com/site/kmmbvnr/_/rsrc/1327390871674/home/django-jenkins-tutorial/jenkins-6.png)

## 參考資料

- [django-jenkins Github](https://github.com/kmmbvnr/django-jenkins) 
- [django-jenkins Tutorial](https://sites.google.com/site/kmmbvnr/home/django-jenkins-tutorial)

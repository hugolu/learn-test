# Jenkins

Jenkins is an award-winning, cross-platform, **continuous integration** and **continuous delivery** application that increases your productivity. Use Jenkins to build and test your software projects continuously making it easier for developers to integrate changes to the project, and making it easier for users to obtain a fresh build. It also allows you to continuously deliver your software by providing powerful ways to define your build pipelines and integrating with a large number of testing and deployment technologies. - 摘錄 [Jenkins](https://wiki.jenkins-ci.org/display/JENKINS/Meet+Jenkins) 官網介紹

## 安裝

參考: https://wiki.jenkins-ci.org/display/JENKINS/Installing+Jenkins+on+Ubuntu

依照官網說明安裝 Jenkins 非常簡單
```shell
$ wget -q -O - https://jenkins-ci.org/debian/jenkins-ci.org.key | sudo apt-key add -
$ sudo sh -c 'echo deb http://pkg.jenkins-ci.org/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
$ sudo apt-get update
$ sudo apt-get install jenkins
```

安裝完後，Jenkins 預設已經啟動
```shell
$ ps aux | grep jenkins
jenkins  10670  0.0  0.0  18596   172 ?        S    16:27   0:00 /usr/bin/daemon --name=jenkins --inherit --env=JENKINS_HOME=/var/lib/jenkins --output=/var/log/jenkins/jenkins.log --pidfile=/var/run/jenkins/jenkins.pid -- /usr/bin/java -Djava.awt.headless=true -jar /usr/share/jenkins/jenkins.war --webroot=/var/cache/jenkins/war --httpPort=8080 --ajp13Port=-1
jenkins  10671  9.9 35.4 1186188 179532 ?      Sl   16:27   0:34 /usr/bin/java -Djava.awt.headless=true -jar /usr/share/jenkins/jenkins.war --webroot=/var/cache/jenkins/war --httpPort=8080 --ajp13Port=-1
vagrant  10752  0.0  0.4  12720  2124 pts/1    S+   16:33   0:00 grep --color=auto jenkins
```

手動設定 Jenkins 服務
```shell
$ sudo service jenkins start        # 啟動
$ sudo service jenkins stop         # 停止
$ sudo service jenkins restart      # 重新啟動
```

## 啟動與存取

參考: https://wiki.jenkins-ci.org/display/JENKINS/Starting+and+Accessing+Jenkins

啟動 Jenkins 最簡單的方式
```shell
$ java -jar jenkins.war
```

打開瀏覽器，開啟 http://192.168.33.10:8080/ (192.168.33.10 是[虛擬機](environment.md)的IP)，就能看到管理介面

### 變更語言

啟動 Jenkins 後，因為瀏覽器語系關係為顯示為中文操作介面，想改成與官網說明一樣的英文介面，依照下面步驟

- 安裝插件：「管理 Jenkins」→「管理外掛程式」→「過濾條件」輸入 `locale` →「下載並於重新啟動後安裝」
- 變更語系：「管理 Jenkins」→「設定系統」→「預設語言」輸入 `en_US` →「Ignore browser preference and force this language to all users」

![Jenkins](jenkins.png)

### Jenkins 功能階層圖
```
Jenkins Home
    |-- Jenkins configure
    |-- Build Jobs
        |-- Job_A
        |   |-- Job Configure
        |   |-- Build History
        |       |-- Build #1
        |       |-- Build #2
        |       |-- Build #3
        |-- Job_B
        |-- Job_C
```

## 實驗一：“Hello World”

### 練習目標

- 建立簡單的 Build Job
- 手動執行 Build Job
- 自動執行 Build Job

### 建立 Build Job

- 到 Jenkins 首頁，點選「New Item」
- 「Item name」填入 `myBuild`，選擇「Freestyle project」，接著進入設定 Build Job 細節頁面
    - 「Build」內按下「Add build step」，選擇「Execute shell」，「Command」填入下面 shell script
    - 按下「Save」儲存離開

```shell
#!/bin/bash
echo "Hello World"
```

### 手動執行

- 到「myBuild」頁面，點選「Build Now」
- 看到「Build History」出現 Build item，點選 #1
    - 點選「Console Output」，看到以下 Build process

```
Started by user anonymous
Building in workspace /var/lib/jenkins/jobs/myProject/workspace
[workspace] $ /bin/bash /tmp/hudson6372466822262253605.sh
Hello World
Finished: SUCCESS
```

### 自動執行 (週期)

- 到「myBuild」頁面，點選「Configure」
    - 「Build Triggers」下點選「Build periodically」，「Schedule」填入 `* * * * *` (表示每分鐘 build 一次)
    - 按下「Save」儲存離開
- 等待數分鐘，看到「Build History」出現多個 Build item

## 實驗二：配合 SCM 進行自動化建置

### 練習目標

- 在開發環境上
    - 建立專案，設定 Git repository

- 在 Jenkins Server 上
    - 安裝 plugin (Git)
    - 隨著 Git repository 更新，進行自動化建置

### 建立專案

在開發環境上，建立工作目錄
```shell
$ mkdir myWorkspace
$ cd myWorkspace
```

設定 Python 版本
```shell
$ pyenv local 3.5.1
$ python --version
Python 3.5.1
```

建立虛擬環境
```shell
$ pyvenv venv
```

切換虛擬環境
```shell
$ pyvenv venv
$ source venv/bin/activate
(venv) $ pip install --upgrade pip
```

> 出現 (venv) 提示表示目前使用 Python virtualenv，往後範例省略顯示

建立專案目錄
```shell
$ mkdir myProject
$ cd myProject
$ pwd
/home/vagrant/myWorkspace/myProject
```

產生 HelloWorld.py
```shell
$ echo 'print("Hello World")' > HelloWorld.py
$ python HelloWorld.py
Hello World
```

初始化 Git repository
```shell
$ git init
```

將 HelloWorld.py 加入 Git repository
```shell
$ git add .
$ git commit -m "add a python file"
```

### 設定 Jenkins Server

安裝 Git plugin

- 到 Jenkins 首頁，選擇「Manage Jenkins」
    - 點選「Manage Plugins」，進入設定插件管理頁面
        - 選擇「Available」標籤，「filter」輸入 `Git plugin`
        - 選取「Git plugin」，按下「Install without restart」
        - 等候安裝完成

修改 Build Job

- 到「myBuild」頁面，點選「Configure」
    - 「Source Code Management」下選擇「Git」，「Repository URL」填入 `file:///home/vagrant/myWorkspace/myProject`
    - 「Build Triggers」，取消「Build periodically」，改選取「Poll SCM」，「Schedule」填入 `* * * * *` (表示每分鐘查詢 git repository 一次，如果 git repository 有更新則觸發 Build Job)
    - 「Build」下「Execute shell」，「Command」改成下面 shell script
    - 按下「Save」儲存離開

```shell
#!/bin/bash
python --version
python HelloWorld.py
```

如果 git repository 在 Jenkins Server 上未建置過、或有任何更新，會在一分鐘內看到自動執行的 Build result

```shell
Started by an SCM change
Building in workspace /var/lib/jenkins/jobs/myProject/workspace
Cloning the remote Git repository
Cloning repository file:///home/vagrant/myWorkspace/myProject
 > git init /var/lib/jenkins/jobs/myProject/workspace # timeout=10
Fetching upstream changes from file:///home/vagrant/myWorkspace/myProject
 > git --version # timeout=10
 > git -c core.askpass=true fetch --tags --progress file:///home/vagrant/myWorkspace/myProject +refs/heads/*:refs/remotes/origin/*
 > git config remote.origin.url file:///home/vagrant/myWorkspace/myProject # timeout=10
 > git config --add remote.origin.fetch +refs/heads/*:refs/remotes/origin/* # timeout=10
 > git config remote.origin.url file:///home/vagrant/myWorkspace/myProject # timeout=10
Fetching upstream changes from file:///home/vagrant/myWorkspace/myProject
 > git -c core.askpass=true fetch --tags --progress file:///home/vagrant/myWorkspace/myProject +refs/heads/*:refs/remotes/origin/*
 > git rev-parse refs/remotes/origin/master^{commit} # timeout=10
 > git rev-parse refs/remotes/origin/origin/master^{commit} # timeout=10
Checking out Revision 8e045c06247802b5d08f757c0a9fe467a3700424 (refs/remotes/origin/master)
 > git config core.sparsecheckout # timeout=10
 > git checkout -f 8e045c06247802b5d08f757c0a9fe467a3700424
First time build. Skipping changelog.
[workspace] $ /bin/bash /tmp/hudson105525603757121577.sh
Python 2.7.9
Hello World
Finished: SUCCESS
```

雖然建置成功，但是 `python --version` 顯示 Python 2.7.9，跟開發環境使用的版本 Python 3.5.1 不同。接下來要讓 Jenkins Server 的執行環境跟開發環境保持一致。

## 實驗三：設定環境

## 實驗四：自動化單元測試

## 實驗五：自動化測試工具







-= TBC =-
----
## 參考
- [Using Jenkins](https://wiki.jenkins-ci.org/display/JENKINS/Use+Jenkins) - Jenkins 官網文件
- [CI (Continuous integration) 關鍵技術：使用 Jenkins](http://www.books.com.tw/products/0010596579) - 偏重 Android App 開發
- [持續整合與自動化測試 - 使用 Jenkins 與 Docker 進行課程實作](https://www.gitbook.com/book/smlsunxie/jenkins-workshop/details) - 內容較完整
- [Jenkins CI 實戰手冊](http://jenkins.readbook.tw/) - 內容不完整
- [Jenkins CI 從入門到實戰講座](http://trunk-studio.kktix.cc/events/jenkins-2016001) - 送電子書，內有詳盡的實作步驟說明
- Automated python unit testing, code coverage and code quality analysis with Jenkins - [part 1](http://bhfsteve.blogspot.tw/2012/04/automated-python-unit-testing-code.html), [part 2](http://bhfsteve.blogspot.tw/2012/04/automated-python-unit-testing-code_20.html), [part 3](http://bhfsteve.blogspot.tw/2012/04/automated-python-unit-testing-code_27.html)
- [基于 Jenkins 的 Python 代码集成整合](http://yumminhuang.github.io/blog/2015/04/17/%E5%9F%BA%E4%BA%8E-jenkins-%E7%9A%84-python-%E4%BB%A3%E7%A0%81%E9%9B%86%E6%88%90%E6%95%B4%E5%90%88/)
- [jenkins集成python的单元测试](http://www.mamicode.com/info-detail-1383168.html)
- [Setup Jenkins, and make it use virtualenv](http://iamnearlythere.com/jenkins-python-virtualenv/)

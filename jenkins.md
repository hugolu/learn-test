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

### 建立專案

- 到 Jenkins 首頁，點選「New Item」
- 「Item name」填入 `myProject`，選擇「Freestyle project」，接著進入設定 Build Job 細節頁面
    - 「Build」內按下「Add build step」，選擇「Execute shell」，「Command」填入下面 shell script
    - 按下「Save」儲存離開

```shell
#!/bin/bash
echo "Hello World"
```

### 手動執行

- 到「myProject」頁面，點選「Build Now」
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

- 到「ProjectOne」頁面，點選「Configure」
    - 「Build Triggers」下點選「Build periodically」，「Schedule」填入 `* * * * *` (表示每分鐘 build 一次)
    - 按下「Save」儲存離開
- 等待數分鐘，看到「Build History」出現多個 Build item

## 實驗二：配合 SCM 進行自動化建置

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

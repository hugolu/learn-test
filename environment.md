# 實驗環境

## 安裝虛擬機器

- [VirtualBox](https://www.virtualbox.org/) 虛擬機器
- [Vagrant](https://www.vagrantup.com/) 虛擬機器管理工具

## 下載作業系統影像檔

到 [Vagrantbox](http://www.vagrantbox.es/) 查詢適當的作業系統，我用 "debian jessie" 關鍵字查詢找到 "Debian Jessie 8.1.0 Release x64"

```shell
$ vagrant box add https://atlas.hashicorp.com/ARTACK/boxes/debian-jessie
$ vagrant box list
ARTACK/debian-jessie                     (virtualbox, 8.1.0)
debian7.8.0                              (virtualbox, 0)
opentable/win-2008r2-standard-amd64-nocm (virtualbox, 1.0.1)
ubuntu/trusty64                          (virtualbox, 20151020.0.0)
```

初始化設定，啟動機器後登入系統
```shell
$ mkdir test
$ cd test
$ vagrant init ARTACK/debian-jessie
$ vagrant up
$ vagrant ssh
```

## 安裝基本套件

```shell
$ sudo apt-get update
$ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm git
```

## 安裝 python

```shell
$ sudo apt-get install python3.4
```

## 安裝 [pip](https://pip.pypa.io/en/stable/) python 套件管理程式

```shell
$ sudo apt-get install python-pip
```

## 檢查 python 版本

```shell
$ python --version
Python 2.7.9
$ which python
/usr/bin/python
$ ls -al /usr/bin/python*
lrwxrwxrwx 1 root root       9 Mar 16  2015 /usr/bin/python -> python2.7
lrwxrwxrwx 1 root root       9 Mar 16  2015 /usr/bin/python2 -> python2.7
-rwxr-xr-x 1 root root 3785928 Mar  1  2015 /usr/bin/python2.7
-rwxr-xr-x 2 root root 4476488 Oct  8  2014 /usr/bin/python3.4
-rwxr-xr-x 2 root root 4476488 Oct  8  2014 /usr/bin/python3.4m
```

## 透過 [pyenv](http://blog.codylab.com/python-pyenv-management/) 管理 python 版本

```shell
$ git clone https://github.com/yyuu/pyenv.git ~/.pyenv
$ git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
$ sudo pip install virtualenv
```

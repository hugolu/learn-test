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

初始化設定
```shell
$ mkdir test
$ cd test
$ vagrant init ARTACK/debian-jessie
```

因為將來要弄一個 web server，為了讓 host os 可以連接，需要產生一個 private network 介面，修改 Vagrantfile 加入下面一行
```
config.vm.network "private_network", ip: "192.168.33.10"
```

啟動機器後登入系統
```shell
$ vagrant up
$ vagrant ssh
```

## 安裝基本套件

```shell
$ sudo apt-get update
$ sudo apt-get install -y make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm git
```

## 安裝 pip - python 套件管理程式

- [安裝 PIP 來管理 Python Packages](https://blog.longwin.com.tw/2014/08/python-setup-pip-package-2014/)
- [pip](https://pip.pypa.io/en/stable/)

```shell
$ sudo apt-get install python-pip
```

## 安裝 pyenv - python 版本管理程式

- [使用 Pyenv 管理多個 Python 版本](http://blog.codylab.com/python-pyenv-management/)
- [pyenv 教程](https://wp-lai.gitbooks.io/learn-python/content/0MOOC/pyenv.html)

```shell
$ git clone https://github.com/yyuu/pyenv.git ~/.pyenv
$ git clone https://github.com/yyuu/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
$ sudo pip install virtualenv
```

添加以下內容到 `~/.bashrc`
```
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

重新載入 `~/.bashrc`
```shell
$ source ~/.bashrc
```

查看可用的 python 版本
```shell
$ pyenv versions
  system
```

列出可用的 python 版本
```shell
$ pyenv install -l
Available versions:
  ...
  3.4.0
  3.4-dev
  3.4.1
  3.4.2
  3.4.3
  3.4.4
  3.5.0
  3.5-dev
  3.5.1
  3.6.0a1
  3.6-dev
  ...
```

安裝 python 3.4.1
```shell
$ pyenv install 3.4.1
$ pyenv versions
  system
* 3.4.1 (set by /home/vagrant/.python-version)
```

切換 python 版本
```shell
$ pyenv version
system (set by /home/vagrant/.python-version)
$ python --version
Python 2.7.9

$ pyenv local 3.4.1

$ pyenv version
3.4.1 (set by /home/vagrant/.python-version)
$ python --version
Python 3.4.1
```

> Python 自 2.1 起開始內建 unittest，積極面可作為測試驅動開發(TDD)，消極面至少提供一個容易上手的測試框架。往後實驗會用到 unittest.mock，這個在 python 2 沒有提供，需要切換到 python 3 才能使用測試替身 (Test Double) 切開相依的元件。

## 安裝 behave - Python BDD framework

```shell
$ pip --version
pip 1.5.6 from /home/vagrant/.pyenv/versions/3.4.1/lib/python3.4/site-packages (python 3.4)
$ pip install behave
pip install -U behave
```

## 安裝 Django - 

- [How to get Django](https://www.djangoproject.com/download/)

```shell
$ pip install Django==1.9.7
```

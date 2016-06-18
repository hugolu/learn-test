# MySQL connector for Python 

目前找到兩種
- [MySQL Connector](https://www.mysql.com/products/connector/) - 由 MySQL 官方提供
- [MyMySQL Connector](https://github.com/PyMySQL/PyMySQL) - 第三方維護，純 Python code

## MySQL Connector

- [MySQL Connector/Python Developer Guide](https://dev.mysql.com/doc/connector-python/en/) - mysql 官方說明

### 搜尋適合版本
- [Index of Packages Matching 'mysql-connector'](https://pypi.python.org/pypi?%3Aaction=search&term=mysql-connector&submit=search)

找到 mysql-connector-python 2.0.4

### 下載
- [mysql-connector-python 2.0.4](https://pypi.python.org/pypi/mysql-connector-python/2.0.4)

下載壓縮檔
```shell
$ wget http://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-2.0.4.zip#md5=3df394d89300db95163f17c843ef49df
```

解壓縮
```shell
$ unzip mysql-connector-python-2.0.4.zip
```

### 安裝
- [MySQL Connector/Python Developer Guide](http://dev.mysql.com/doc/connector-python/en/)
- [Installing Connector/Python from a Source Distribution](http://dev.mysql.com/doc/connector-python/en/connector-python-installation-source.html)

```shell
$ python setup.py install
```

### 測試
```
$ python
Python 3.5.1 (default, Jun  9 2016, 17:09:39)
[GCC 4.9.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import mysql.connector
>>>
```

或是在 test/account/ 目錄，執行以下單元測試
```shell
$ python -m unittest -v account1
test_login_with_correct_username_password (account1.TestAccount) ... ok
test_login_with_invalid_password (account1.TestAccount) ... ok
test_login_with_invalid_username (account1.TestAccount) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.004s

OK
```

## PyMySQL Connector

- [PyMySQL github](https://github.com/PyMySQL/PyMySQL)

### 安裝
```shell
$ pip install PyMySQL
```

### 測試
```shell
$ python
Python 3.5.1 (default, Jun  9 2016, 17:09:39)
[GCC 4.9.2] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import pymysql.cursors
>>>
```

或是在 test/account/ 目錄，執行以下單元測試
```shell
$ python -m unittest -v account2.py
test_login_with_correct_username_password (account2.TestAccount) ... ok
test_login_with_invalid_password (account2.TestAccount) ... ok
test_login_with_invalid_username (account2.TestAccount) ... ok

----------------------------------------------------------------------
Ran 3 tests in 0.004s

OK
```

# sqlite 快速瀏覽

這份文件快速瀏覽 SQLite 基本語法，包含創建資料庫、創建表格，新增、更新、查詢、刪除記錄 (CURD)。

## 參考資料

- [SQLite 教程](http://www.runoob.com/sqlite/sqlite-tutorial.html)
- [SQLite 官網](https://www.sqlite.org/)

## 創建資料庫
- http://www.runoob.com/sqlite/sqlite-create-database.html

在當前目錄產生一個 testDB.db 檔案作為 SQLite 資料庫。
```shell
$ sqlite3 testDB.db
SQLite version 3.8.7.1 2014-10-29 13:59:56
Enter ".help" for usage hints.
sqlite>
```

使用 `.databases` 命令列出資料庫的檔案名稱
```sql
sqlite> .database
seq  name             file
---  ---------------  ----------------------------------------------------------
0    main             /tmp/sqlite/testDB.db
```

使用 `.quit` 退出資料庫
```sql
sqlite> .quit
```

## 創建表格
- http://www.runoob.com/sqlite/sqlite-create-table.html

建立 `COMPANY` 與 `DEPARTMENT` 兩個表格
```sql
sqlite> CREATE TABLE COMPANY (
   ...> ID INT PRIMARY KEY  NOT NULL,
   ...> NAME    TEXT NOT    NULL,
   ...> AGE     INT NOT     NULL,
   ...> ADDRESS CHAR(50),
   ...> SALARY  REAL
   ...> );
sqlite> CREATE TABLE DEPARTMENT (
   ...> ID INT PRIMARY KEY  NOT NULL,
   ...> DEPT    CHAR(50)    NOT NULL,
   ...> EMP_ID  INT         NOT NULL
   ...> );
```

使用 `.tables` 列出表格
```sql
sqlite> .tables
COMPANY     DEPARTMENT
```

使用 `.schema` 顯示表格結構
```sql
sqlite> .schema COMPANY
CREATE TABLE COMPANY (
ID INT PRIMARY KEY  NOT NULL,
NAME    TEXT NOT    NULL,
AGE     INT NOT     NULL,
ADDRESS CHAR(50),
SALARY  REAL
);
```

## 插入紀錄
- http://www.runoob.com/sqlite/sqlite-insert.html

方法一
```sql
sqlite> INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
   ...> VALUES (1, 'Paul', 32, 'California', 20000.00 );
sqlite> INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
   ...> VALUES (2, 'Allen', 25, 'Texas', 15000.00 );
sqlite>
sqlite> INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
   ...> VALUES (3, 'Teddy', 23, 'Norway', 20000.00 );
sqlite>
sqlite> INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
   ...> VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 );
sqlite>
sqlite> INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
   ...> VALUES (5, 'David', 27, 'Texas', 85000.00 );
sqlite>
sqlite> INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY)
   ...> VALUES (6, 'Kim', 22, 'South-Hall', 45000.00 );
```

方法二
```sql
sqlite> INSERT INTO COMPANY VALUES (7, 'James', 24, 'Houston', 10000.00 );
```

## 查詢記錄
- http://www.runoob.com/sqlite/sqlite-select.html

使用 `SELECT` 查詢表格資料
```sql
sqlite> SELECT * FROM COMPANY;
1|Paul|32|California|20000.0
2|Allen|25|Texas|15000.0
3|Teddy|23|Norway|20000.0
4|Mark|25|Rich-Mond |65000.0
5|David|27|Texas|85000.0
6|Kim|22|South-Hall|45000.0
7|James|24|Houston|10000.0
```

使用 `.header on` 命令顯示表格標頭，使用 `.mode column` 排列欄位，提高表格可讀性
```sql
sqlite> .header on
sqlite> .mode column
sqlite> SELECT * FROM COMPANY;
ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
1           Paul        32          California  20000.0
2           Allen       25          Texas       15000.0
3           Teddy       23          Norway      20000.0
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0
6           Kim         22          South-Hall  45000.0
7           James       24          Houston     10000.0
```

## 更新紀錄
- http://www.runoob.com/sqlite/sqlite-update.html

使用 `UPDATE` 更新紀錄內容，用 `WHERE` 找出更新對象
```sql
sqlite> UPDATE COMPANY SET ADDRESS = 'Texas' WHERE ID = 6;
sqlite> SELECT * FROM COMPANY;
ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
1           Paul        32          California  20000.0
2           Allen       25          Texas       15000.0
3           Teddy       23          Norway      20000.0
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0
6           Kim         22          Texas       45000.0
7           James       24          Houston     10000.0
```

## 刪除記錄
- http://www.runoob.com/sqlite/sqlite-delete.html

使用 `DELETE` 刪除紀錄，用 `WHERE` 找出刪除對象
```sql
sqlite> DELETE FROM COMPANY WHERE ID = 7;
sqlite> SELECT * FROM COMPANY;
ID          NAME        AGE         ADDRESS     SALARY
----------  ----------  ----------  ----------  ----------
1           Paul        32          California  20000.0
2           Allen       25          Texas       15000.0
3           Teddy       23          Norway      20000.0
4           Mark        25          Rich-Mond   65000.0
5           David       27          Texas       85000.0
6           Kim         22          Texas       45000.0
```

## 刪除表格
- http://www.runoob.com/sqlite/sqlite-drop-table.html

刪除表格前，列出目前的表格
```sql
sqlite> .tables
COMPANY     DEPARTMENT
```

使用 `DROP TABLE` 刪除表格
```sql
sqlite> DROP TABLE DEPARTMENT;
sqlite> .tables
COMPANY
```

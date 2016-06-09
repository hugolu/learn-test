# sqlite

參考資料

- [SQLite 语法](http://www.runoob.com/sqlite/sqlite-syntax.html)
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

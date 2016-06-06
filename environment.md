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

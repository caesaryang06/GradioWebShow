pushcode.bat pushcode.sh  这两个脚本

这两个脚本作用是：
1. pushcode.bat：用于在Windows系统上执行git push命令，将代码推送到远程仓库。【包括github和gitee两个仓库】
2. pushcode.sh：用于在Linux或Mac系统上执行git push命令，将代码推送到远程仓库。

这两个脚本都包含了git push命令，用于将代码推送到远程仓库。在Windows系统上，使用pushcode.bat脚本；在Linux或Mac系统上，使用pushcode.sh脚本。

pushcode.bat脚本：
```bash
@echo off
git add .
git commit -m "update"
git push
```
pushcode.sh脚本：
```bash
#!/bin/bash
git add .
git commit -m "update"
git push
```

这两个脚本都包含了三个命令：
1. git add .：将所有修改过的文件添加到暂存区。`.`表示当前目录下的所有文件。
2. git commit -m "update"：提交暂存区中的文件，并添加提交信息"update"。
3. git push：将本地仓库中的文件推送到远程仓库。

使用这两个脚本，可以方便地将代码推送到远程仓库，而不需要手动执行git add、git commit和git push命令。



【注意】
要使用这两个脚本  需要在本地仓库中配置好远程仓库的地址，并且已经安装了git。
配置远程仓库的地址的命令是：
```bash
git remote add origin <远程仓库地址>
```
其中，`<远程仓库地址>`是远程仓库的地址，可以是github或gitee等。

样例 
添加github远程仓库命令：
  git remote add github https://github.com/caesaryang06/pydemo.git
添加gitee远程仓库命令：
  git remote add gitee https://gitee.com/caesaryang06/pydemo.git




  命令介绍

添加远程仓库到本地
git remote add origin https://github.com/caesaryang06/pydemo.git

查看远程仓库
git remote -v

删除远程仓库
git remote remove origin


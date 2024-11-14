:: 该脚本用于脚本将远程仓库添加到本地仓库  【包含gitee和github】
:: 仓库地址格式为：https://gitee.com/xxx/xxx.git
:: 仓库地址格式为：https://github.com/xxx/xxx.git
@echo off
:: 初始化当前目录为git仓库
git init
:: 添加github远程仓库到本地
git remote add github https://github.com/caesaryang06/pydemo.git
:: 添加gitee远程仓库到本地
git remote add gitee https://gitee.com/caesaryang06/pydemo.git


git remote add github https://github.com/caesaryang06/GradioWebShow.git

git remote add gitee https://gitee.com/caesaryang/gradio-web-show.git
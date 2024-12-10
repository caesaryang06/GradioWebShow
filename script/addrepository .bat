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


:: 需要说明的是  如果是在新环境执行 在提交代码的时候需要输入用户名和密码 

::   做如下设置  
::   git config --global user.name "caesaryang06"
::   git config --global user.email "caesaryang06@163.com"
::   git config --global credential.helper store
::
::   首次提交需要输入用户名和密码【密码为token 需在网站申请】
::   git push github master   输入用户名为 caesaryang06  密码为token
::   
::   注意 用户名跟上面不同
::   git push gitee master   输入用户名为 caesaryang  密码为token
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
::
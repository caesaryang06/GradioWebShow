@echo off

:: 更新requirements.txt
pip freeze > requirements.txt


:: 代码提交并发布到远程仓库【github，gitee】
git pull github master
git add .
git commit -m "auto - commit"
git push github master
git push gitee master
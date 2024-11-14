@echo off

:: 更新requirements.txt
pip freeze > requirements.txt

:: 加密文件
python encrypt4file.py encrypt4file


:: 代码提交并发布到远程仓库【github，gitee】
git add .
git commit -m "auto - commit"
git push github master
git push gitee master
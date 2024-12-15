from apscheduler.schedulers.blocking import BlockingScheduler
import subprocess
import os
import sys
from datetime import datetime
import encrypt4file



LAST_TIME = ""


# 定义要执行的任务函数

def my_task(key, repo_path):
    global LAST_TIME
    current_datetime1 = datetime.now()
    print(f"定时任务执行开始...【{current_datetime1}】")
    os.chdir(repo_path)

    file_stat = os.stat('data.db')
    modification_time_seconds = str(file_stat.st_mtime)
    if modification_time_seconds != LAST_TIME:
        
        # 加密文件
        encrypt4file.encrypt4file(key)

        subprocess.run(["git", "add", "db/encrypted.db"])
        subprocess.run(["git", "commit", "-m", "自动提交：更新代码"])
        subprocess.run(["git", "push", "github", "master"])
        subprocess.run(["git", "push", "gitee", "master"])

        LAST_TIME = modification_time_seconds
    else:
        print("文件未修改，无需提交")


    current_datetime2 = datetime.now()
    print(f"定时任务执行结束...【{current_datetime2}】")






if __name__ == "__main__":

    if len(sys.argv) > 2:
        key = sys.argv[1]
        repo_path = sys.argv[2]
        print("key:", key)
        print("repo_path:", repo_path)
    else:
        print("请输入key和repo_path")


    # 创建调度器对象
    scheduler = BlockingScheduler()

    # 添加定时任务，这里设置为每隔5秒执行一次my_task函数
    scheduler.add_job(my_task, 'interval', seconds=1800,args=[key, repo_path])

    # 启动调度器
    scheduler.start()


import subprocess


'''
脚本说明：  该脚本用于加密数据库文件，并提交到github和gitee
'''




def run_exe(exe_path, args=None, cwd=None, env=None):
    """
    运行本地 EXE 程序

    Args:
        exe_path: EXE 文件的路径
        args: 传递给 EXE 程序的参数，以列表形式提供
        cwd: 指定运行时的工作目录
        env: 指定运行时环境变量
    """

    try:
        subprocess.run([exe_path] + args, cwd=cwd, env=env, check=True)
    except subprocess.CalledProcessError as e:
        print(f"执行失败: {e}")






def git_commit(repo_path, message):
  """
  提交代码到本地 Git 仓库

  Args:
    repo_path: Git 仓库的路径
    message: 提交信息
  """

  try:
    # 进入仓库目录
    subprocess.run(['cd', repo_path], shell=True, check=True)
    # 添加所有更改
    subprocess.run(['git', 'add', './encrypted.db'], check=True)
    # 提交更改
    subprocess.run(['git', 'commit', '-m', message], check=True)
    # 推送到github
    subprocess.run(['git', 'push', 'github', 'master'], check=True)
    # 推送到gitee
    subprocess.run(['git', 'push', 'gitee', 'master'], check=True)

    print("代码提交成功！")
  except subprocess.CalledProcessError as e:
    print(f"提交失败：{e}")




def main():

    # 加密文件
    run_exe("D:/soft/Windows加密解密工具.exe",
            ["1", "011019", "D:/vscode-pro/GradioWebShow/data.db", "D:/vscode-pro/GradioWebShow/encrypted.db"], cwd="C:/Users/yangxinmin")

   
    # 提交加密后的数据库文件到github和gitee
    git_commit("D:/vscode-pro/GradioWebShow", "update")


if __name__ == "__main__":
    main()

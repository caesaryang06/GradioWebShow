import requests
import subprocess
import psutil
import os
import json

class FunctionProcessor:
    def __init__(self, inputFiles, output_folder):
        """
        构造器，初始化输入文件夹和输出文件夹路径
        """
        self.inputFiles = inputFiles
        self.output_folder = output_folder
        self.dict = {
            "提取字幕文件": self.batch_extract_subtitle,
        }

    # 定义函数 启动exe本地程序
    def start_exe(self,json):
        """
        判断指定的exe是否已经启动，如果未启动则启动它
        :param  json对象  要包含key: exe_name; value为：可执行文件的名称（包含.exe后缀）
        """
        exe_name = json["exe_name"]
        is_running = False
        for proc in psutil.process_iter():
            try:
                if proc.name().lower() == exe_name.lower():
                    is_running = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        if not is_running:
            os.system(exe_name)
            print(f"{exe_name} 已启动")
        else:
            print(f"{exe_name} 已经在运行，无需启动")


    # 定义函数  媒体转文本
    def media2text(self,api_url, media_path, response_format, language="auto", model="medium"):
        """
        调用参数样例 json对象   {
            "api_url": "http://192.168.1.2:5000/api/v1/whisper",
            "media_path": "C:/Users/zheng/Desktop/2023-11-27-11-30-23.mp4",
            "response_format": "text",
            "language": "auto",
            "model": "medium"
        }
        language: 语言代码:可选如下

            >
            > 中文：zh
            > 英语：en
            > 法语：fr
            > 德语：de
            > 日语：ja
            > 韩语：ko
            > 俄语：ru
            > 西班牙语：es
            > 泰国语：th
            > 意大利语：it
            > 葡萄牙语：pt
            > 越南语：vi
            > 阿拉伯语：ar
            > 土耳其语：tr
            >

        model: 模型名称，可选如下
            >
            > base 对应于 models/models--Systran--faster-whisper-base
            > small 对应于 models/models--Systran--faster-whisper-small
            > medium 对应于 models/models--Systran--faster-whisper-medium
            > large-v3 对应于 models/models--Systran--faster-whisper-large-v3
            >

            说明  medium.en  字幕确定为英文

        response_format: 返回的字幕格式，可选 text|json|srt

        file: 音视频文件，二进制上传
        
        """
        # 请求参数  file:音视频文件，language：语言代码，model：模型，response_format:text|json|srt
        # 返回 code==0 成功，其他失败，msg==成功为ok，其他失败原因，data=识别后返回文字
        files = {"file": open(media_path, "rb")}
        data = {"language": language, "model": model,
                "response_format": response_format}
        response = requests.request(
            "POST", api_url, timeout=600, data=data, files=files)
       
        json_data = json.loads(response.text)
        if json_data['code'] == 0:
           return 0, json_data['data']
        else:
           return 1, json_data['msg']
      
    # 定义函数  视频下载   下载工具  https://github.com/soimort/you-get/tree/develop
    def download_video(self, url, save_path):
        """
        # 调用you-get下载视频
        # -o 指定下载路径
        # -O 指定输出文件名
        # -d 指定下载整个视频列表
        # -p 指定下载视频的清晰度
        # --format 指定下载视频的格式
        # --no-caption 不下载字幕
        # --no-merge 不合并视频和音频
        # --debug 输出调试信息
        # --json 输出JSON格式的信息
        # --info 输出视频信息
        # --version 输出you-get版本信息
        # --help 输出you-get帮助信息
        调用样例： command = ['you-get', url, '-o', './videos', '-O', 'test.mp4','-p', '1080p', '--no-caption', '--no-merge', '--debug']
                subprocess.call(command)
        """

        command = ['you-get', url, '-o', './videos', '-O', 'test.mp4',
                   '-p', '1080p', '--no-caption', '--no-merge', '--debug']
        subprocess.call(command)
        

    
    # 批量处理提取字幕   response_format, language="auto", model="medium"
    def batch_extract_subtitle(self, json):
        """
        批量处理提取字幕
        :param json对象  样例  {'api_url': 'http://127.0.0.1:9977/api','response_format':'srt','language':'auto','model':'medium'}
        :return:
        """
        api_url = json["api_url"]
        response_format = json["response_format"]
        language = json["language"]
        model = json["model"]
        result = []
        for inputFile in self.inputFiles:
            print(f"正在处理 {inputFile}")
            # 调用函数提取字幕
            code,data = self.media2text(api_url, inputFile, response_format, language, model)
            if code == 0:
                # 将结果保存到文件
                saveFile = os.path.join(
                    self.output_folder, os.path.basename(inputFile) + ".srt")
                with open(saveFile, "w", encoding="utf-8") as f:
                    f.write(data)
                print(f"已提取 {inputFile} 的字幕，并临时保存到 {self.output_folder}")

                result.append(saveFile)
            else:
                print(f"提取 {inputFile} 的字幕失败，错误信息：{data}")


        return result        
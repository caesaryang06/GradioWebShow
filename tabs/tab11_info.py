import gradio as gr
import sqlite3
from tools import customer_common_funcs as ccf
import pandas as pd
import asyncio
from tools.azure_local_service import AzureTextToSpeech
import os


voices_info = [
    ( "zh-CN-YunxiNeural", "男性", "大陆普通话"),
    ( "zh-CN-XiaochenNeural", "女性", "大陆普通话"),
    ("en-US-Brian:DragonHDLatestNeural", "男性", "美式英语"),
    ("en-US-Aria:DragonHDLatestNeural", "女性", "美式英语"),

]


#获取密钥
subscription_key = os.environ.get('AZURE_SUBSCRIPTION_KEY')
# 获取分区
region = os.environ.get('AZURE_REGION')
tts = AzureTextToSpeech(subscription_key, region)


def get_voices():
    return [f"{voice}--{gender}--{description}" for voice, gender, description in voices_info]

# 处理提交事件
def submit_result(languageinfo, text):


    #删除指定目录下的内容
    ccf.delete_folder_contents("out/azure/tmp")

    audio_file = "out/azure/tmp/output.wav"

    tts.text_to_speech(text, audio_file, languageinfo.split("--")[0])

    return audio_file



def func():
    with gr.Row():
        with gr.Column():
            Language_drop = gr.Dropdown(
                choices=get_voices(), label="选择语言", interactive=True, allow_custom_value=True)
            text_input = gr.TextArea(label="文本内容")
            submit_btn = gr.Button("提交", variant="primary")
        with gr.Column():
            out_audio = gr.Audio(label="音频", type="filepath", interactive=False)

    # 提交事件
    submit_btn.click(fn=submit_result, inputs=[
                     Language_drop, text_input], outputs=[out_audio])

import gradio as gr
from tools import customer_common_funcs as ccf
import os 


SHOW_COUNT = 30


# 处理提交事件
def submit_result(Language, Gender):

    # 指定路径
    sampledir = f"data/azure_voice_samples/{Language}/{Gender}"

    # 获取指定路径的所有样本音频文件
    list_files = ccf.list_files_in_directory(sampledir)

    if len(list_files) > SHOW_COUNT:
        list_files = list_files[:SHOW_COUNT]

    results = []

    for i, file in enumerate(list_files):
        Voice = file.split(".")[0].replace("_", ":")
        results.append(gr.Audio(f"{sampledir}/{file}", visible=True, label=Voice))

    for i in range(SHOW_COUNT - len(results)):
        results.append(gr.Audio(visible=False))

    return results


def func():
    with gr.Row():
        with gr.Column():
            Language_drop = gr.Dropdown(
                choices=["zh-CN", "en-US"], label="选择语言", interactive=True, allow_custom_value=True, value="zh-CN")
        with gr.Column():
            Gender_drop = gr.Dropdown(
                choices=["Male", "Male"], label="选择性别", interactive=True, allow_custom_value=True, value="Male")
        with gr.Column():
            submit_btn = gr.Button("提交", variant="primary")
    with gr.Row():
        # 创建多个音频播放器和复制按钮的组合
        audio_outputs = []
        for i in range(SHOW_COUNT):  # 假设我们要显示6个音频
            if i == 0:
                with gr.Row():
                    audio = gr.Audio(
                        label=f"音频 {i+1}",
                        type="filepath",
                        interactive=False,
                    )
            else:
                with gr.Row():
                    audio = gr.Audio(
                        label=f"音频 {i+1}",
                        type="filepath",
                        interactive=False,
                        visible=False,
                    )

            audio_outputs.append(audio)
  
    # 提交事件
    submit_btn.click(fn=submit_result, inputs=[
                     Language_drop, Gender_drop], outputs=audio_outputs)

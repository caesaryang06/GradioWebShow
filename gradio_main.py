import gradio as gr
from tabs import tab1_info, tab2_info, tab5_info, tab6_info, tab8_info, tab9_info, tab10_info, tab11_info, tab12_info, tab13_info, tab14_info, tab15_info
import sys

# 加载 .env 文件
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())



# 登录验证函数
def login(username, password):
    return username == "admin" and password == "admin"


if __name__ == "__main__":

    with gr.Blocks() as app:
        with gr.Tabs():
            with gr.Tab("生成随机密码"):
                tab1_info.func()
            with gr.Tab("密码加解密"):
                tab2_info.func()
            with gr.Tab("邮箱管理"):
                tab5_info.func()
            with gr.Tab("软件账号管理"):
                tab6_info.func()
            with gr.Tab("长短链接转换"):
                tab8_info.func()
            with gr.Tab("提示词管理"):
                tab9_info.func()
            with gr.Tab("提示词优化工具"):
                tab14_info.func()
            with gr.Tab("语音实验室"):
                tab10_info.func()
            with gr.Tab("AZURE文本转语音"):
                tab11_info.func()
            with gr.Tab("PDF2EXCEL"):
                tab12_info.func()
            with gr.Tab("comfyui工作流"):
                tab13_info.func()   
            with gr.Tab("工作流"):
                tab15_info.func()

    # 若在google云盘启动  使用如下代码
    #app.launch(inbrowser=True, auth=login, share=True)
        

    # 本地运行代码
    app.launch(inbrowser=True, auth=login, share=False)

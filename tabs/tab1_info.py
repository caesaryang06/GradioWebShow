import gradio as gr
from tools import custom_codec as cc


def submit_result():
    # 生成随机密码和随机密码加密后的结果
    # 获取随机密码
    random_passwd = cc.getRandomPassword()

    return random_passwd


def clear_result():
    return ""


def func():
    with gr.Row():
        with gr.Column():
            input_text = gr.Textbox(
                label="default", interactive=False, visible=False)
            with gr.Row():
                with gr.Column():
                    clear_btn = gr.Button(value="清空")
                with gr.Column():
                    submit_btn = gr.Button("生成", variant="primary")
        with gr.Column():
            output_text1 = gr.Textbox(label="密码")

    # 设置清空点击事件
    clear_btn.click(fn=clear_result, inputs=[], outputs=[
                    output_text1])

    # 设置提交点击事件
    submit_btn.click(fn=submit_result, inputs=[],
                     outputs=[output_text1])

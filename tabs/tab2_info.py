import gradio as gr
from tools import custom_codec as cc
from tools.encryption_tool import EncryptionUtils
from tools import customer_common_funcs as ccf


def submit_result(op, key, input):
    """
    自定义加解密
    输入: 操作类型,输入文本
    输出: 输出文本
    """

    # 定义函数字典
    dict = {
        "加密": EncryptionUtils.encrypt,
        "解密": EncryptionUtils.decrypt
    }

    func_name = dict[op]

    if func_name:
        return func_name(ccf.getkey(key), input)
    else:
        return "无效的操作类型"


def clear_result():
    return "", ""


def func():
    with gr.Row():
        with gr.Column():
            op_radio = gr.Radio(["加密", "解密"],
                                label="操作类型", info="请选择操作类型:", value="解密")
            input_key = gr.Textbox(label="key")
            input_text = gr.Textbox(label="输入")
            with gr.Row():
                with gr.Column():
                    clear_btn = gr.Button(value="清空")
                with gr.Column():
                    submit_btn = gr.Button("提交", variant="primary")
        with gr.Column():
            output_text = gr.Textbox(label="结果")

    # 设置清空点击事件
    clear_btn.click(fn=clear_result, inputs=[], outputs=[
                    input_text, output_text])

    # 设置提交点击事件
    submit_btn.click(fn=submit_result, inputs=[op_radio, input_key,input_text], outputs=[output_text])
import gradio as gr
from tools import customer_common_funcs as ccf
import os 



# 处理提交事件
def submit_result(input_files):


    #删除指定目录下的内容
    ccf.delete_folder_contents("out/pdf/tmp")


    list = []

    # 处理文件
    for file in input_files:
        # 获取原文件名（不包括扩展名）
        base_name = os.path.splitext(os.path.basename(file))[0]
        excelfile =  f"out/pdf/tmp/{base_name}.xlsx"
        ccf.extract_table_from_pdf(file, excelfile)
        list.append(excelfile)

    # 将结果列表中的所有文件压缩成一个zip文件
    basedir = "out/pdf/tmp/"
    zip_name = basedir + ccf.getCurrentDateStr() + ".zip"
    ccf.zip_all_files(list, zip_name)

    return list, zip_name



def func():
    with gr.Row():
        with gr.Column():
            input_files = gr.File(label="上传单个或者多个pdf文件", file_count="multiple")
            submit_btn = gr.Button("提交", variant="primary")
        with gr.Column():
            output = gr.File(label="输出文件明细", file_count="multiple")
            zip_output = gr.File(label="输出压缩文件")

    # 提交事件
    submit_btn.click(fn=submit_result, inputs=[
                     input_files], outputs=[output,zip_output])

import gradio as gr
from tools.workflow_tools import FunctionProcessor
import json
from tools import customer_common_funcs as ccf
from playsound import playsound


# 函数及参数配置
FUNCTIONS_PARAMS = {
    "提取字幕文件": {'api_url': 'http://127.0.0.1:9977/api', 'response_format': 'srt', 'language': 'auto', 'model': 'medium'},
    "add_prefix": ["prefix"],
    "replace_text": ["old", "new"],
    "truncate": ["length"]
}



# 执行工作流
def execute_workflow(input_files, function_dropdown, function_params):
    print(f"执行参数  {function_dropdown} {function_params}")
    output_folder = "out/flow/tmp"
    #删除指定目录下的内容
    ccf.delete_folder_contents(output_folder)
    processor = FunctionProcessor(input_files, output_folder)
    lists = processor.dict[function_dropdown](json.loads(function_params))
    zip_name = f"{function_dropdown}_{ccf.getCurrentDateStr()}.zip"

    # 完成后音量提醒
    playsound("data/音频/铃声.mp3")
    return "执行完成", ccf.zip_all_files(lists, zip_name)



def func():

    # 输入和输出文件夹布局
    input_files = gr.File(label="输入多个文件", file_count="multiple")
       
    gr.Markdown("### 配置函数和参数")
    with gr.Row():
        function_dropdown = gr.Dropdown(
            label="函数", choices=list(FUNCTIONS_PARAMS.keys()), value="提取字幕文件")
        param_input = gr.TextArea(
            label="参数 (JSON 格式)", value=json.dumps(FUNCTIONS_PARAMS["提取字幕文件"], ensure_ascii=False))
    with gr.Row():
        exec_button = gr.Button("执行", variant="primary")
    result = gr.Textbox(label="结果", interactive=False)
    zip_output = gr.File(label="输出压缩文件")


    # 执行工作流
    exec_button.click(
        execute_workflow,
        inputs=[input_files, function_dropdown, param_input],
        outputs=[result,zip_output]
    )


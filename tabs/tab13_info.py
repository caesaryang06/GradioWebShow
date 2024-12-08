import gradio as gr
from tools import customer_common_funcs as ccf
import sqlite3
import json
import requests
import pandas as pd
import re

# 假设ComfyUI API的URL
API_URL = "http://127.0.0.1:8188/prompt"

# 执行工作流


def queue_prompt(api_url, prompt):
    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    response = requests.post(api_url, data=data)
    return response.text


# 读取 comfyui workflow 信息
def get_comfyui_workflow():

    # 连接到SQLite数据库
    conn = sqlite3.connect('data.db')
    # 读取表数据到DataFrame
    workflowDF = pd.read_sql(
        'SELECT workflow,inputs,content FROM comfyui_workflow', conn)

    return workflowDF

def read_workflows():
    return pd.read_excel("工作流.xlsx")

# 根据input "[12]['input']['text']" 从json对象中获取value值


def get_value_from_json(json_obj, input_str):
    result = re.findall(r"\d+|[a-zA-Z_]+", input_str)
    return json_obj[result[0]][result[1]][result[2]]

# 设置输入项


def set_value_for_json(json_obj, input_key, input_value):
    result = re.findall(r"\d+|[a-zA-Z_]+", input_key)
    json_obj[result[0]][result[1]][result[2]] = input_value


# 导入工作流
def import_workflow(json_file, import_records, workflow_name):
    work_names = []
    try:
        with open(json_file.name, 'r') as file:
            json_data = json.load(file)
        df = get_comfyui_workflow()
        records = [x.strip() for x in import_records['key']]

        # 如果工作流名称不存在  则添加  如果已经存在 则更新
        if (df[df['workflow'] == workflow_name].empty):
            df.loc[len(df.index)] = [workflow_name, ';'.join(records),
                                     ccf.base64_encode(json.dumps(json_data, ensure_ascii=False))]
        else:
            df.loc[df['workflow'] == workflow_name, [
                'inputs', 'content']] = [';'.join(records), ccf.base64_encode(json.dumps(json_data, ensure_ascii=False))]

        #  按照 工作流名称去重
        df.drop_duplicates(subset=['workflow'],
                        keep='first', inplace=True)

        # 保存数据
        # 连接到SQLite数据库
        conn = sqlite3.connect('data.db')
        df.to_sql('comfyui_workflow', conn, if_exists='replace', index=False)

        work_names = df['workflow'].unique().tolist()
        return f"Workflows imported successfully: {workflow_name}", gr.Dropdown(choices=work_names, interactive=True)
    except Exception as e:
        return f"Error importing workflow: {workflow_name}", gr.Dropdown(choices=work_names, interactive=True)


# 获取工作流的输入项
def get_workflow_inputs(workflow_name):
    df = get_comfyui_workflow()
    work_names = df['workflow'].unique().tolist()
    if workflow_name not in work_names:
        return "Workflow not found."

    # 处理
    inputs = df[df['workflow'] == workflow_name]['inputs'].values[0]
    content = df[df['workflow'] == workflow_name]['content'].values[0]
    jsonobj = json.loads(ccf.base64_decode(content))
    keys = []
    values = []
    for input in inputs.split(';'):
        value = get_value_from_json(jsonobj, input)
        keys.append(input)
        values.append(value)

    return gr.Dataframe(value=pd.DataFrame({'key': keys, 'value': values}), interactive=True)


# 执行工作流
def execute_workflow(api_input, workflow_name, edit_records):

    df = get_comfyui_workflow()

    content = df[df['workflow'] == workflow_name]['content'].values[0]
    jsonobj = json.loads(ccf.base64_decode(content))

    for index, row in edit_records.iterrows():
        key = row['key']
        value = row['value']
        set_value_for_json(jsonobj, key, value)

    # 调用api 发送json
    queue_prompt(api_input, jsonobj)
    return "发送成功"


# 删除工作流
def delete_workflow(workflow_name):
    df = get_comfyui_workflow()
    df = df[df['workflow'] != workflow_name]
    conn = sqlite3.connect('data.db')
    df.to_sql('comfyui_workflow', conn, if_exists='replace', index=False)
    return "删除成功"


# 导入/执行工作流单选框修改执行函数
def change_show(value):
    if value == "导入工作流":
        return gr.File(visible=True), gr.DateTime(visible=True), gr.Button(visible=True), gr.Button(visible=True), gr.Textbox(visible=True), gr.Button(visible=True), gr.Textbox(visible=False), gr.Dropdown(visible=False), gr.Dataframe(visible=False), gr.Button(visible=False), gr.Button(visible=False), gr.Textbox(visible=True, value="")
    else:
        df = get_comfyui_workflow()
        work_names = df['workflow'].unique().tolist()
        return gr.File(visible=False), gr.DateTime(visible=False), gr.Button(visible=False), gr.Button(visible=False), gr.Textbox(visible=False), gr.Button(visible=False), gr.Textbox(visible=True, interactive=True), gr.Dropdown(choices=work_names, visible=True), gr.Dataframe(visible=True), gr.Button(visible=True), gr.Button(visible=True), gr.Textbox(visible=True, value="")

# 添加新行执行函数
def add_record(inputs):
    records = [x for x in inputs['key']]
    records.append("")
    return gr.DataFrame(value=pd.DataFrame({'key': records}), headers=["key"], interactive=True)

# 删除最后行执行函数
def delete_record(inputs):
    records = [x for x in inputs['key']]
    return gr.DataFrame(value=pd.DataFrame({'key': records[:-1]}), headers=["key"], interactive=True)



def func():
    switch_show = gr.Radio(
        label="导入/执行工作流", choices=["导入工作流", "执行工作流"], value="导入工作流")
    json_file_input = gr.File(file_count="single", label="Upload ComfyUI JSON")
    import_records = gr.Dataframe(label="添加要修改输入项的key", value=pd.DataFrame(
        {'key': [""]}), headers=["key"], interactive=True)
    with gr.Row():
        with gr.Column():
            add_buttion = gr.Button("添加新行", variant="primary")
        with gr.Column():
            delete_button = gr.Button("删除最后行", variant="primary")
    workflow_name_input = gr.Textbox(label="Workflow Name")
    import_button = gr.Button("Import Workflow", variant="primary")
    api_input = gr.Textbox(label="API URL", value=API_URL, visible=False)
    workflow_list = gr.Dropdown(label="Select Workflow", visible=False)
    edit_records = gr.Dataframe(label="编辑输入项", value=pd.DataFrame(
        {'key': [""], 'values': [""]}), headers=["key", "value"], interactive=True, visible=False)
    execute_button = gr.Button("Execute", visible=False, variant="primary")
    with gr.Row():
        with gr.Column():
            execute_button = gr.Button(
                "运行工作流", visible=False, variant="primary")
        with gr.Column():
            delete_workflow_button = gr.Button("删除工作流", variant="primary",visible=False)
    output = gr.Textbox(label="Output")

    import_button.click(import_workflow, inputs=[
                        json_file_input, import_records, workflow_name_input], outputs=[output, workflow_list])
    
    workflow_list.change(get_workflow_inputs, inputs=[
                         workflow_list], outputs=[edit_records])
    
    execute_button.click(execute_workflow, inputs=[
                         api_input, workflow_list, edit_records], outputs=[output])
    
    delete_workflow_button.click(delete_workflow, inputs=[
                                 workflow_list], outputs=[output])


    switch_show.change(change_show, [switch_show], [json_file_input, import_records, add_buttion, delete_button,
                       workflow_name_input, import_button, api_input, workflow_list, edit_records, execute_button, delete_workflow_button, output])

    # 添加新行
    add_buttion.click(add_record, inputs=[
                      import_records], outputs=[import_records])

    # 删除最后行
    delete_button.click(delete_record, inputs=[
                        import_records], outputs=[import_records])

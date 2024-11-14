import gradio as gr
import sqlite3
from tools import customer_common_funcs as ccf
import pandas as pd

# 获取提示词表信息


def get_prompts():

    # 连接到SQLite数据库
    conn = sqlite3.connect('data.db')
    # 读取表数据到DataFrame
    promptDF = pd.read_sql(
        'SELECT uuid,category,serial_number,prompt FROM prompt_table', conn)

    return promptDF


# 获取分类信息
def get_category():

    df = get_prompts()

    return df['category'].unique().tolist()


# 保存提示词并返回指定分类的提示词
def save_prompt(promptDF):
    # 连接到SQLite数据库
    conn = sqlite3.connect('data.db')
    # 保存数据
    promptDF.to_sql('prompt_table', conn, if_exists='replace', index=False)


# 根据分类获取提示词
def get_prompt_by_category(category, df):

    dataDF = df[df['category'] ==
                category].sort_values(by='serial_number')
    resultDF = dataDF[['category', 'serial_number', 'prompt']].rename(
        columns={'category': '分类', 'serial_number': '序号', 'prompt': '提示词'})
    return resultDF


def refresh_result():
    return gr.Dropdown(choices=get_category(), interactive=True)


def change_result(category, seq):

    df = get_prompts()

    dataDF = df[(df['category'] == category) & (df['serial_number'] == seq)]

    if dataDF.empty:
        return ""
    else:
        return dataDF['prompt'].values[0]


def category_change_result(category):
    rsultDF = get_prompt_by_category(category, get_prompts())
    return rsultDF, ccf.export_to_excel(rsultDF)


def add_prompt(category, seq, prompt):

    df = get_prompts()
    # 这里需要判断  如果 df 存在 分类 和 序号 相同的记录 则更新对应的记录 如果不存在 则添加
    if (df[(df['category'] == category) & (df['serial_number'] == seq)].empty):
        df.loc[len(df.index)] = [ccf.get_unique_value(
            category + f'{seq}'), category, seq, prompt]
    else:
        df.loc[(df['category'] == category) & (
            df['serial_number'] == seq), ['prompt']] = [prompt]

    # 保存数据
    save_prompt(df)

    # 根据分类获取提示词
    resultDF = get_prompt_by_category(category, df)

    return resultDF, ccf.export_to_excel(resultDF)


def delete_prompt(category, seq):
    df = get_prompts()
    df = df.drop(df[(df['category'] == category) &
                 (df['serial_number'] == seq)].index)

    # 保存数据
    save_prompt(df)

    # 根据分类获取提示词
    resultDF = get_prompt_by_category(category, df)

    return resultDF, ccf.export_to_excel(resultDF)


def all_result():

    df = get_prompts()

    resultDF = df[['category', 'serial_number', 'prompt']].rename(
        columns={'category': '分类', 'serial_number': '序号', 'prompt': '提示词'})

    return resultDF, ccf.export_to_excel(resultDF)


def func():
    with gr.Row():
        category_drop = gr.Dropdown(
            choices=get_category(), label="选择分类", interactive=True, allow_custom_value=True)
        refresh_btn = gr.Button(
            value="刷新", icon="icon/refresh.icon", size="sm")
        seq_input = gr.Textbox(label="指定序号")
        prompt_input = gr.TextArea(label="输入新的提示词")
    with gr.Row():
        add_button = gr.Button("添加提示词", variant="primary")
        delete_button = gr.Button("删除提示词", variant="primary")
        all_button = gr.Button("全部提示词", variant="primary")

    output = gr.Dataframe(label="Table", headers=[
        "分类", "序号", "提示词"])
    download_file = gr.File(label="结果下载")

    # 刷新按钮点击事件
    refresh_btn.click(fn=refresh_result, inputs=[], outputs=[category_drop])

    # 分类改变事件
    category_drop.change(fn=category_change_result, inputs=[
                         category_drop], outputs=[output, download_file])

    # 改变序号的事件
    seq_input.change(fn=change_result, inputs=[
                     category_drop, seq_input], outputs=[prompt_input])

    add_button.click(
        add_prompt,
        inputs=[category_drop, seq_input, prompt_input],
        outputs=[output, download_file]
    )

    # 删除事件
    delete_button.click(fn=delete_prompt, inputs=[
                        category_drop, seq_input], outputs=[output, download_file])

    # 获取全部提示词
    all_button.click(fn=all_result, inputs=[], outputs=[output, download_file])

import gradio as gr
import pyshorteners
import pyperclip
import sqlite3
import pandas as pd
from tools import customer_common_funcs as ccf
import re


# 初始化 URL 缩短器
shortener = pyshorteners.Shortener()


# 获取长短链接
def get_url_mappings():
    # 连接到SQLite数据库
    conn = sqlite3.connect('data.db')
    # 读取表数据到DataFrame
    urlMappingDF = pd.read_sql(
        'SELECT uuid,short_url,long_url FROM url_mapping', conn)

    return urlMappingDF


# 保存长短链接
def save_url_mapping(short_url, long_url):
    urlMappingDF =get_url_mappings()

    urlMappingDF.loc[len(urlMappingDF.index)] = [ccf.get_unique_value(short_url +
                                                  long_url), short_url, long_url]
    
    #  按照 软件名称 和 邮箱名称 去重
    urlMappingDF.drop_duplicates(subset=['short_url', 'long_url'],
                       keep='first', inplace=True)

    # 保存数据
    # 连接到SQLite数据库
    conn = sqlite3.connect('data.db')
    urlMappingDF.to_sql('url_mapping', conn,
                        if_exists='replace', index=False)



def long_to_short(long_url):
    try:
        short_url = shortener.tinyurl.short(long_url)
        return short_url
    except Exception as e:
        return f"发生错误: {str(e)}"


def short_to_long(short_url):
    try:
        long_url = shortener.tinyurl.expand(short_url)
        return long_url
    except Exception as e:
        return f"发生错误: {str(e)}"


def submit_result(op_radio, input_link):
    if op_radio == "长链接 → 短链接":
        short_link = long_to_short(input_link)

        pattern = re.search(r'https?://[^\s;]+', short_link)
        if pattern:
            # 保存长短链接
            save_url_mapping(short_link, input_link)
           
        return short_link
    elif op_radio == "短链接 → 长链接":
        return short_to_long(input_link)



def copy_result(text):
    pyperclip.copy(text)
    print(f"已将【{text}】复制到剪贴板")
    


def func():
    op_radio = gr.Radio(["长链接 → 短链接", "短链接 → 长链接"],
                            label="操作类型", value="长链接 → 短链接")
    input_link = gr.Textbox(label="请输入链接", show_copy_button=True,show_label=True)
    
    submit_btn = gr.Button("转换",variant="primary")

    result_output = gr.Textbox(
        label="转换结果", interactive=False, show_copy_button=True, show_label=True)
    copy_btn = gr.Button("复制结果", variant="secondary")

    submit_btn.click(
        submit_result,
        inputs=[op_radio, input_link],
        outputs=[result_output]
    )

    copy_btn.click(copy_result, inputs=[result_output], outputs=[])

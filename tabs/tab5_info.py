import gradio as gr
import pandas as pd
import sqlite3
import tempfile
from tools.encryption_tool import EncryptionUtils
from tools import customer_common_funcs as ccf



# 获取邮箱
def get_emails():

    # 连接到SQLite数据库
    conn = sqlite3.connect('data.db')
    # 读取表数据到DataFrame
    emailsDF = pd.read_sql(
        'SELECT email_address,email_password FROM emails', conn)

    return emailsDF


def add_row(address_input, password_input, search_input):
    df = get_emails()
    new_row = pd.DataFrame(
        {'email_address': [address_input], 'email_password': [EncryptionUtils.encrypt(ccf.getkey('011019'), password_input)]})
    df = pd.concat([df, new_row], ignore_index=True)

    # 去重操作
    df.drop_duplicates(subset='email_address', inplace=True)

    # 更新数据库
    conn = sqlite3.connect('data.db')
    df.to_sql('emails', conn, if_exists='replace', index=False)

    return df, ccf.export_to_excel(df)


def delete_row(address_input, password_input, search_input):
    df = get_emails()
    df = df[df['email_address'] != address_input]

    # 去重操作
    df.drop_duplicates(subset='email_address', inplace=True)

    # 更新数据库
    conn = sqlite3.connect('data.db')
    df.to_sql('emails', conn, if_exists='replace', index=False)

    return df, ccf.export_to_excel(df)


def update_row(address_input, password_input, search_input):
    df = get_emails()
    df.loc[df['email_address'] == address_input,
           ['email_password']] = [EncryptionUtils.encrypt(ccf.getkey('011019'), password_input)]

    # 去重操作
    df.drop_duplicates(subset='email_address', inplace=True)

    # 更新数据库
    conn = sqlite3.connect('data.db')
    df.to_sql('emails', conn, if_exists='replace', index=False)

    return df, ccf.export_to_excel(df)


def search(address_input, password_input, search_input):
    df = get_emails()
    data = df[df['email_address'].str.contains(search_input, case=False)]
    return data, ccf.export_to_excel(data)


def show_table(address_input, password_input, search_input):
    df = get_emails()
    return df, ccf.export_to_excel(df)


def export_to_excel(df):
    # 创建一个临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx') as tmp:
        df.to_excel(tmp.name, index=False)
        tmp_path = tmp.name
    return tmp_path



def func():
    with gr.Row():
        address_input = gr.Textbox(label="邮箱地址")
        password_input = gr.Textbox(label="邮箱密码")
        search_input = gr.Textbox(label="邮箱地址模糊搜索")

    with gr.Row():
        add_button = gr.Button("新增记录", variant="primary")
        del_button = gr.Button("删除记录", variant="primary")
        update_button = gr.Button("修改记录", variant="primary")
        search_button = gr.Button("搜索记录", variant="primary")
        all_button = gr.Button("全部记录", variant="primary")

    output = gr.Dataframe(label="Table")
    download_file = gr.File(label="结果下载")

    add_button.click(
        add_row,
        inputs=[address_input, password_input, search_input],
        outputs=[output, download_file]
    )

    del_button.click(
        delete_row,
        inputs=[address_input, password_input, search_input],
        outputs=[output, download_file]
    )

    update_button.click(
        update_row,
        inputs=[address_input, password_input, search_input],
        outputs=[output, download_file]
    )

    search_button.click(
        search,
        inputs=[address_input, password_input, search_input],
        outputs=[output, download_file]
    )

    all_button.click(
        show_table,
        inputs=[address_input, password_input, search_input],
        outputs=[output, download_file]
    )

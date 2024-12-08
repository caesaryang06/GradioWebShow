from tools.sql4sqlite import SqliteTool
from tools import customer_common_funcs as ccf
import pandas as pd
import sqlite3
import os 
from tools.encryption_tool import *


def createTable():
    db = SqliteTool('data.db')
    db.delete_table('comfyui_workflow')
    db.create_table('comfyui_workflow',
                    'workflow TEXT NOT NULL,inputs TEXT NOT NULL,content TEXT NOT NULL')



def insert():
    db = SqliteTool('data.db')
    db.insert('prompt_table', {'uuid': '1234',
              'category': 'a', 'serial_number': 1, 'prompt': 'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'})
    db.insert('prompt_table', {'uuid': '1235',
                               'category': 'a', 'serial_number': 2, 'prompt': 'ccccccccccccccccccccccccccccccccccccc'})
    db.insert('prompt_table', {'uuid': '1236',
                               'category': 'a', 'serial_number': 3, 'prompt': 'dddddddddddddddddddddddddddddddddddddddd'})
    
   

def delete_record():
    db = SqliteTool('data.db')
    db.delete("url_mapping",
              "uuid='03a017cdadb6c4a1f487dcaa5e3493ddf9eff724e737bf1c195892d9b0726d1b'")


def demo01():
    EncryptionUtils.encrypt_file('data.db', 'encrypted.db')


def demo02():
    key = 'KuCecPma4NaOBOoaFMe_lH_iki5xS6SK3738dPnsd98='
    EncryptionUtils.decrypt_file(key, 'encrypted.db', 'test.db')


if __name__ == '__main__':
    createTable()
    #insert()
    #delete_record()
    # demo01()
    # demo02()
    # conn = sqlite3.connect('test.db')
    # # 读取表数据到DataFrame
    # promptDF = pd.read_sql(
    #     'SELECT uuid,category,serial_number,prompt FROM prompt_table', conn)
    
    # print(promptDF)
    # key = os.environ.get('DB_ENCRYPTION_KEY')
    # print(key)


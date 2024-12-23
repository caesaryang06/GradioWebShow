from tools.sql4sqlite import SqliteTool
from tools import customer_common_funcs as ccf
import pandas as pd
import sqlite3
import os 
from tools.encryption_tool import *



# 若不存在  则为添加  若存在  则忽略创建操作
def createTable():
    '''
    若不存在  则为添加  若存在  则忽略创建操作
    '''
    db = SqliteTool('data.db')

    # emails
    db.create_table('emails',
                    'email_address TEXT, email_password TEXT')
    

    # url_mapping
    db.create_table('url_mapping',
                    'uuid TEXT, short_url TEXT, long_url TEXT')
    

    # prompt_table
    db.create_table('prompt_table',
                    'uuid TEXT, category TEXT, serial_number TEXT, prompt TEXT')
    
    # comfyui_workflow
    db.create_table('comfyui_workflow',
                    'workflow TEXT NOT NULL,inputs TEXT NOT NULL,content TEXT NOT NULL')
    
    # software_accounts
    db.create_table('software_accounts',
                    'uuid TEXT, software_name TEXT, account TEXT, password TEXT, is_available TEXT, remark TEXT')
    
    # workflow_configs
    db.create_table('workflow_configs',
                    'workflow TEXT, inputDir TEXT, outputDir TEXT, functionName TEXT, funcParams TEXT, remark TEXT')

    db.delete_table('workflow_configs')

if __name__ == '__main__':
    createTable()



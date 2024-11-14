import shutil
import os
import math
import os
import uuid
import time
import datetime
import hashlib
import tempfile
import zipfile


# 传入dataframe导出数据到Excel文件
def export_to_excel(df):
    '''
    传入dataframe导出数据到Excel文件
    '''

    # 删除指定目录下文件名称小于当天的文件
    delete_old_files('out/excel')


    excelFile = 'out/excel/' + getCurrentDateTImeStr() + '.xlsx'
    df.to_excel(excelFile, index=False)

    return excelFile


def delete_old_files(directory):
    today = datetime.date.today()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            # 从文件名中提取日期部分（假设文件名格式为 YYYYMMDD.extension）
            file_date = datetime.date(int(filename[:4]), int(
                filename[4:6]), int(filename[6:8]))
            if file_date < today:
                os.remove(file_path)
                print(f"Deleted {file_path}")





# 获取唯一值
def get_unique_value(s):
    m = hashlib.sha256()
    m.update(s.encode('utf-8'))
    return m.hexdigest()



# 获取key
def getkey(key):
    return key + '7890123456'


# 返回指定路径下的所有文件名称
def list_files_in_directory(directory_path):
    """
    返回指定路径下的所有文件名称

    Args:
    directory_path (str): The path to the directory from which to list files.

    Returns:
    list: A list of file names in the directory.
    """
    file_names = []  # Initialize an empty list to store file names
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)  # Create full path
        if os.path.isfile(file_path):  # Check if it is a file
            file_names.append(filename)
    return file_names


# 获取当前日期，格式为"YYYYMMDD"
def getCurrentDateStr():
    """
    获取当前日期，格式为"YYYYMMDD"
    """
    today = datetime.date.today()
    return str(today).replace("-", "")

# 获取当前日期和时间，格式为"YYYYMMDDHHMMSS"
def getCurrentDateTImeStr():
    """
    获取当前日期和时间，格式为"YYYYMMDDHHMMSS"
    """
    now = datetime.datetime.now()
    return now.strftime('%Y%m%d%H%M%S')


# 传入多个变量返回第一个不为None的值
def first_not_none(*args):
    """
    传入多个变量返回第一个不为None的值
    """
    for arg in args:
        if arg is not None:
            return arg
    return None


# 获取当前时间戳
def get_current_timestamp():
    return int(time.time())


# 获取uuid
def get_uuid():
    return str(uuid.uuid4())


# 获取指定路径下文件的个数
def count_files(directory_path):
    # 计数变量初始化
    file_count = 0

    # 遍历指定目录下的所有文件和文件夹
    for entry in os.listdir(directory_path):
        # 拼接完整的文件或文件夹路径
        full_path = os.path.join(directory_path, entry)

        # 检查这个路径是否是文件
        if os.path.isfile(full_path):
            file_count += 1

    return file_count



# 计算文本中包含多少个{}
def count_brackets(text):
    """
    计算文本中包含多少个{}
    """
    return text.count('{}')



# 删除指定文件夹内的所有内容
def delete_folder_contents(folder_path):
    """
    删除指定文件夹下的所有内容
    """
        # 检查文件夹是否存在  
    if os.path.exists(folder_path):  
        # 删除文件夹及其所有内容  
        shutil.rmtree(folder_path)  
        print(f"文件夹 {folder_path} 及其所有内容已被删除。")  
    else:  
        print(f"文件夹 {folder_path} 不存在。")

    os.makedirs(folder_path)
    print(f"文件夹 {folder_path} 已成功创建。")



# 将多个文件压缩成一个zip文件
def zip_all_files(files, zip_name):
    '''
    # 将多个文件压缩成一个zip文件
    :param files: 文件列表
    :param zip_name: 压缩文件名
    '''
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in files:
            zipf.write(file)














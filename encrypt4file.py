from tools.encryption_tool import EncryptionUtils
import sys
# 该Python文件用加解密


def encrypt4file():
    # 加密文件
    EncryptionUtils.encrypt_file('data.db', 'encrypted.db')



def decrypt4file():
    # 解密文件
    EncryptionUtils.decrypt_file('encrypted.db', 'data.db')




if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == "encrypt4file":
        encrypt4file()
    elif len(sys.argv) > 1 and sys.argv[1] == "decrypt4file":
        decrypt4file()
    else:
        print("请输入正确的命令 encrypt4file 或 decrypt4file")

from tools import customer_common_funcs as ccf 
from tools.encryption_tool import EncryptionUtils
import sys
# 该Python文件用加解密


DECRYPT_KEY = "gw6u7qf3U8xKVzRn78fuLA==Liucg5cCV2KZnThbjWUEgMHfyZUmB3wdEjJqgDK3Dpueb1bKVC3VZ/jyw/IMGO29"


def encrypt4file(keystr):

    key = EncryptionUtils.decrypt(ccf.getkey(keystr), DECRYPT_KEY)

    # 加密文件
    EncryptionUtils.encrypt_file(key, 'data.db', 'encrypted.db')


def decrypt4file(keystr):

    key = EncryptionUtils.decrypt(ccf.getkey(keystr), DECRYPT_KEY)

    # 解密文件
    EncryptionUtils.decrypt_file(key, 'db/encrypted.db', 'data.db')




if __name__ == '__main__':

    if len(sys.argv) > 2:
        # 参数获取
        keystr = sys.argv[2]
    else:
        # 控制台输入密钥
        keystr = input("请输入密钥: ")
    print("keystr: ", keystr)

    if len(sys.argv) > 1 and sys.argv[1] == "encrypt4file":
        encrypt4file(keystr)
    elif len(sys.argv) > 1 and sys.argv[1] == "decrypt4file":
        decrypt4file(keystr)
    else:
        print("请输入正确的命令 encrypt4file 或 decrypt4file")

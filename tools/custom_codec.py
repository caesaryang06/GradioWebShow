#!/usr/bin/python
import random

list1=['!','@','#','$','%','&','*','<','>','/']
list2=['y', 'p', 'e', 'u', 'q', 'd', 'x', 'l', 'a', 's', 'i', 'm', 'o', 'g', 't']
list3=['B', 'K', 'O', 'D', 'F', 'G', 'X', 'Z', 'N', 'H', 'C', 'J', 'U', 'M', 'Y']
list4=['7', '3', '1', '9', '6', '8', '2', '4', '5','0']

metaData = [list1,list2,list3,list4]


## 定义密码规则   两个大写  两个小写    六个数字    一个特殊符号
## 获取密码
## 解码


# 获取随机密码
def getRandomPassword():
    '''
     获取随机密码
     定义密码规则   两个大写  两个小写    六个数字    一个特殊符号
    :return:  随机两个大写 + 随机两个小写 + 随机六个数字 + 随机一个特殊字符
    '''
    str1 = "".join(random.choices(list3,k=2))
    str2 = "".join(random.choices(list2,k=2))
    str3 = "".join(random.choices(list4,k=6))
    str4 = "".join(random.choices(list1))
    return str1 + str2 + str3 + str4


def encodePassword(password):
    '''
    对密码进行编码处理
    :param password:
    :return:
    '''
    result = []
    for pChar in password:
        for i in range(len(metaData)):
            list = metaData[i]
            if pChar in list:
                index = list.index(pChar)
                str = hex(index).replace('0x','')
                result.append(f'{i}{str}')
                break

            if i == 3 and pChar not in list:
                raise BaseException('编码失败！该密码中包含无法编码的字符')


    return ''.join(result)


def decodePassword(encodePassword):
    '''
    解密该自定义编码后的密码
    :return:
    '''
    result = []
    list = [ encodePassword[i*2:i*2+2] for i in range(len(encodePassword)//2) ]
    for str in list:
        i = int(str[0])
        j = int('0x'+str[1],base=16)
        result.append(metaData[i][j])

    return "".join(result)




if __name__ == '__main__':
    # 获取随机密码
    # print(getRandomPassword())

    ## 对密码进行编码
    encodeStr = encodePassword('Yxm011019')
    print(encodeStr)

    ## 对密码进行解码
    print(decodePassword(encodeStr))

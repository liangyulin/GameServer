# -*- coding:utf-8 -*-
"""
encode, decode, convert等公用部分
"""
import json

import sys


def decode(buff_str, n = sys.maxint):
    """
    处理buff_str, 返回body部分真正的payload string
    n用来限定读取几个消息, 比如n=1, 只读取一个消息(login时候)
    """
    if isinstance(buff_str, str):
        res_list = []
        count = 0
        while len(buff_str) > 2 and count < n:
            if buff_str[0:2] == '\r\n':
                index = buff_str.index('\r\n', 2)
                payload_length = int(buff_str[2:index])
                if len(buff_str) >= index + 2 + payload_length:
                    payload_str = buff_str[index + 2:index + 2 + payload_length]
                    res_list.append(json.loads(payload_str))
                    next_start = index + 2 + payload_length
                    if next_start >= len(buff_str):  # out of bound, string ends
                        buff_str = ""
                        break
                    buff_str = buff_str[next_start:]
                    count += 1
                else:
                    break
            else:
                break
        return res_list, buff_str


def encode(d):
    jstr = json.dumps(d)
    header = '\r\n' + str(len(jstr)) + '\r\n'
    return header + jstr


def encode_content(content, code='msg'):
    jstr = json.dumps({'code': code, 'content': content, 'sender': 'system'})
    header = '\r\n' + str(len(jstr)) + '\r\n'
    return header + jstr


def convert_key(obj):
    """
    to transform json.loads dict's unicode key back to str type of key.
    This is a fix for Python2.7's weird unicode type.
    """
    if isinstance(obj, dict):
        return {convert_key(key): convert_key(value) for key, value in obj.iteritems()}
    elif isinstance(obj, list) or isinstance(obj, tuple):
        return [convert_key(ele) for ele in obj]
    elif isinstance(obj, unicode):
        return obj.encode('utf-8')
    else:
        return obj


if __name__ == '__main__':
    str1 = '\r\n2\r\n{}\r\n2\r\n{}\r\n28\r\n{"code":"gidle", "value":23}\r\n2\r\n{}'
    akey = decode(str1)[0][2].keys()[0]
    print(type(akey))  # if we only decode, then we have unicode-type key
    print(type(convert_key(akey)))  # we use convert_key, then we have str-type key to avoid future troubles
    print(convert_key(decode(str1)))
    print (type(convert_key(decode(str1))[0][2].keys()[0]))
# -*- encoding: utf-8 -*-
"""
@File       : recordInfo.py    
@Contact    : daihepeng@sina.cn
@Repository : https://github.com/phantomdai
@Modify Time: 2021/4/12 9:58 下午
@Author     : phantom
@Version    : 1.0
@Descriptions : record the testing information, including time
"""
import os


def record_time_info(path, info):
    """
    record the infomation of time
    :param path: the target path
    :param info: the testing time infomation
    :return:
    """
    if not os.path.isfile(path):
        raise Exception("please specify a file path")
    else:
        pass

    with open(path, 'a', encoding='utf-8') as f:
        f.write(info)
    f.close()

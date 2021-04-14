# -*- encoding: utf-8 -*-
"""
@File       : WriteSelectedSeeds.py    
@Contact    : daihepeng@sina.cn
@Repository : https://github.com/phantomdai
@Modify Time: 2021/4/12 9:38 下午
@Author     : phantom
@Version    : 1.0
@Descriptions : write selected seeds into specify dir
"""
import os
import shutil


def write_selected_seeds(target_path, selected_seeds):
    """
    write selected seeds into specify dir
    :param target_path: target dir
    :param selected_seeds:  the list of selected seeds
    :return: true: success; false: failed
    """
    if not os.path.isdir(target_path):
        raise Exception("please specify a dir!")
    else:
        pass

    for seed in selected_seeds:
        shutil.copy(seed, os.path.join(target_path, os.path.basename(seed)))



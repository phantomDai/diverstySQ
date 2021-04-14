# -*- encoding: utf-8 -*-
"""
@File       : informationBasedMethod.py    
@Contact    : daihepeng@sina.cn
@Repository : https://github.com/phantomdai
@Modify Time: 2021/4/7 9:14 上午
@Author     : phantom
@Version    : 1.0
@Descriptions : this script is used to create a diversity seed queue according
to information theory
"""

import os
import shutil
import time
import zipfile
import util.WriteSelectedSeeds as myWriter
import util.recordInfo as myRecorder

suite_dir = ''
test_cases_set = []
number_seeds = 0


def create_seed_queue_infoTheory(number, test_cases_dir, seed_dir):
    """
    create a diversity seed queue according to information theory
    :param seed_dir: the dir that saves the selected seeds
    :param number: the number of needed seeds
    :param test_cases_dir: the dir of test cases
    :return: a set of seeds
    """
    if os.path.isdir(test_cases_dir):
        select_seeds(test_cases_dir, seed_dir, number)
    else:
        raise Exception("please check the dir of test cases")


def select_seeds(test_case_dir, seed_dir, number):
    """
    select {number} seeds based on information theory
    :param test_case_dir: the dir of test cases
    :param seed_dir:  the file path that saves the selected seeds
    :param number: the number of needed seeds
    :return: a seed queue
    """
    temp_zip_list = []
    seeds_path = []
    print("create zip files:")
    for root, dirs, filenames in os.walk(test_case_dir):
        for filename in filenames:
            temp_zip_file = zipfile.ZipFile(os.path.join(test_case_dir, filename.replace(".JPEG", ".zip")), 'w', zipfile.ZIP_DEFLATED)
            temp_zip_file.write(os.path.join(root, filename))
            temp_zip_list.append(os.path.join(test_case_dir, filename.replace(".JPEG", ".zip")))
            seeds_path.append(os.path.join(root, filename))
            temp_zip_file.close()

    for i in range(len(seeds_path)):
        seeds_path[i] = (seeds_path[i], os.path.getsize(seeds_path[i].replace(".JPEG", ".zip")))
    seeds_path.sort(key=lambda filename: filename[1], reverse=True)
    print("delete the created zip file")
    for file in temp_zip_list:
        if os.path.exists(file):
            os.remove(file)
        else:
            pass
    print("select the seeds")
    for i in range(number):
        shutil.copy(seeds_path[i][0], os.path.join(seed_dir, os.path.basename(seeds_path[i][0])))


def test():
    start_time = time.clock()
    create_seed_queue_infoTheory(20, "/Users/phantom/dataset/ImageNet/imageNet_test",\
                                 "/Users/phantom/dataset/ImageNet/Infomation_theory")
    end_time = time.clock()
    info = "time: " + str(end_time - start_time)
    myRecorder.record_time_info("/Users/phantom/pythonDir/diverstySQ/results/inforBased.txt", info)


test()
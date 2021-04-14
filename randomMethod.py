# -*- encoding: utf-8 -*-
"""
@File       : randomMethod.py    
@Contact    : daihepeng@sina.cn
@Repository : https://github.com/phantomdai
@Modify Time: 2021/4/12 9:06 下午
@Author     : phantom
@Version    : 1.0
@Descriptions : randomly construct a seed queue
"""

import os
import random
import util.WriteSelectedSeeds as myWriter
import util.recordInfo as myRecorder
import time


def create_seed_queue_random(test_suite_path, num_seeds, random_seed, target_path):
    """
    randomly create a seed queue
    :param test_suite_path: the parent dir of test cases
    :param num_seeds: the number of needed seeds
    :param random_seed: the seed of random
    :param target_path: the dir that save the selected seeds
    :return: null
    """
    all_test_cases = []
    selected_seeds = []
    random.seed(random_seed)
    for root, dirs, filenames in os.walk(test_suite_path):
        for filename in filenames:
            all_test_cases.append(os.path.join(root, filename))

    for _ in range(num_seeds):
        selected_seeds.append(all_test_cases[random.randint(0, len(all_test_cases) - 1)])

    myWriter.write_selected_seeds(target_path, selected_seeds)


def test():
    start_time_1 = time.clock()
    create_seed_queue_random("/Users/phantom/dataset/ImageNet/imageNet_test", 20, 1, \
                             "/Users/phantom/dataset/ImageNet/DLFuzz_random_1")
    end_time_1 = time.clock()
    create_seed_queue_random("/Users/phantom/dataset/ImageNet/imageNet_test", 20, 2, \
                             "/Users/phantom/dataset/ImageNet/DLFuzz_random_2")
    end_time_2 = time.clock()
    create_seed_queue_random("/Users/phantom/dataset/ImageNet/imageNet_test", 20, 3, \
                             "/Users/phantom/dataset/ImageNet/DLFuzz_random_3")
    end_time_3 = time.clock()
    create_seed_queue_random("/Users/phantom/dataset/ImageNet/imageNet_test", 20, 4, \
                             "/Users/phantom/dataset/ImageNet/DLFuzz_random_4")
    end_time_4 = time.clock()
    create_seed_queue_random("/Users/phantom/dataset/ImageNet/imageNet_test", 20, 5, \
                             "/Users/phantom/dataset/ImageNet/DLFuzz_random_5")
    end_time_5 = time.clock()

    time_info = "1: " + str(end_time_1 - start_time_1) + "\n" + "2: " + \
        str(end_time_2 - end_time_1) + "\n" + "3: " + \
        str(end_time_3 - end_time_2) + "\n" + "4: " + \
        str(end_time_4 - end_time_3) + "\n" + "5: " + \
        str(end_time_5 - end_time_4)
    myRecorder.record_time_info("./results/random.txt", time_info)


test()

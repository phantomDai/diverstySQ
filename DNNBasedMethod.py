# -*- encoding: utf-8 -*-
"""
@File       : DNNBasedMethod.py    
@Contact    : daihepeng@sina.cn
@Repository : https://github.com/phantomdai
@Modify Time: 2021/4/8 8:31 下午
@Author     : phantom
@Version    : 1.0
@Descriptions : create seed queue based on VGG19
"""
import time

from keras.applications.vgg19 import VGG19
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
from keras.models import Model
import numpy as np
import random
import os
import util.WriteSelectedSeeds as myWriter
import util.recordInfo as myRecorder

test_cases_path = []  # the paths of all test cases
counter = 0  # the counter of selection test cases
seeds = []  # the paths of selected seeds
size_candidate_seeds = 10  # the size of candidate seeds set


def get_feature(img_dir):
    """
    get the feature of the figure
    :param img_dir: the path of the figure
    :return: the vector of the figure
    """

    base_model = VGG19(weights='imagenet')
    model = Model(input=base_model.input, output=base_model.get_layer('fc2').output)
    img = image.load_img(img_dir, target_size=(224, 224))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    f = model.predict(x)
    # print(f.shape)
    # print(f)
    return f


def cal_distance(f1, f2):
    """
    calculate the distance of f1 and f2
    :param f1: the vector f1
    :param f2: the vector f2
    :return: the value of cosine
    """

    cos1 = np.sum(f1 * f2)
    cos21 = np.sqrt(np.sum(f1 * f1))
    cos22 = np.sqrt(np.sum(f2 * f2))
    return cos1 / float(cos22 * cos21)


def upload_test_suite(test_suite):
    """
    upload the paths of all test cases
    :param test_suite: the paths of all test cases
    :return:
    """
    global test_cases_path
    test_cases_path = test_suite


def select_candidate_test_case(seed_generator):
    """
    randomly select a set of candidate test cases
    :param seed_generator: the generator of seeds
    :return: a set of candidate test cases
    """
    candidate_set = []
    global counter, test_cases_path
    if counter == 0:
        seeds.append(test_cases_path[seed_generator.randint(0, len(test_cases_path) - 1)])
        counter = counter + 1
    else:
        pass

    for i in range(0, size_candidate_seeds):
        candidate_set.append(test_cases_path[seed_generator.randint(0, len(test_cases_path) - 1)])
    return candidate_set


def obtain_new_seed(candidate_test_cases):
    """
    select a seed from candidate test cases
    :param candidate_test_cases: the set of candidate test cases
    :return: null
    """
    max_value = 0.
    max_candidate = ''
    print("calculate distance")
    for candidate_test_case in candidate_test_cases:
        min_value = 1.
        min_candidate = ''
        # 计算候选种子与已选种子中的最小距离
        for seed in seeds:
            print("get the feature of seed:")
            distance_seed_candidate = cal_distance(get_feature(candidate_test_case), get_feature(seed))
            if distance_seed_candidate < min_value:
                min_candidate = candidate_test_case
                min_value = distance_seed_candidate

        if min_value > max_value:
            max_value = min_value
            max_candidate = min_candidate
        else:
            pass

    if max_candidate not in seeds:
        global counter
        counter = counter + 1
        seeds.append(max_candidate)
    else:
        pass


def create_seed_queue_featureBased(test_suite_paths, num_seeds, random_seed, target_dir):
    """
    create seed queue based the deep features of the figures
    :param target_dir: the dir saves the selected seeds
    :param test_suite_paths: all test cases
    :param num_seeds: the number of needed seeds
    :param random_seed: the seed of random
    :return: a seed queue
    for example：
    first the interface upload_test_case(paths) is needed to be used；
    Then create_seed_queue_featureBased([],10,1), where [] is the set of paths of
    test cases; 10 is the number of needed seeds; 1 is the seed of random. Then this method
    will return a list of seeds
    """
    # get all paths of test cases
    upload_test_suite(test_suite_paths)
    random.seed(random_seed)
    global counter
    while counter != num_seeds:
        print("generate candidate test cases")
        candidate_seeds = select_candidate_test_case(random)
        print("obtain a seed from candidate test cases")
        obtain_new_seed(candidate_seeds)

    myWriter.write_selected_seeds(target_dir, seeds)


def test():
    print("start parsing the path of all test cases:")
    all_paths = []
    for root, dirs, filenames in os.walk("/Users/phantom/dataset/ImageNet/imageNet_test"):
        for filename in filenames:
            temp_path = os.path.join(root, filename)
            all_paths.append(temp_path)

    create_seed_queue_featureBased(all_paths, 20, 1, "/Users/phantom/dataset/ImageNet/feature_based_10_1")


start_time = time.clock()
test()
end_time = time.clock()
info = "20_1:" + str(end_time - start_time)
myRecorder.record_time_info("/Users/phantom/pythonDir/diverstySQ/results/DNNBased.txt", info)

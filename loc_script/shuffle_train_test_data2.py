#!/usr/bin/env python
# encoding: utf-8
# Author: tianrong@trio.ai (Tian Rong)

import numpy as np
import sys
import math
import random
#import new_seg

def Shuffle(word_id_data_path):
    data_list = []
    with open(word_id_data_path, 'r') as file_content:
        for line in file_content:
            data_list.append(line)
    #print data_list

    """
    shuffle_indices = np.random.permutation(np.array(data_list))
    #print list(shuffle_indices)
    return list(shuffle_indices)
    """

    index_list = range(0, len(data_list))
    random.shuffle(index_list)
    shuffle_indices = []
    for index in index_list:
        shuffle_indices.append(data_list[index])
    #print shuffle_indices
    return shuffle_indices


def SplitWordIDData2TrainTest(word_id_data, train_set_proportion,
        test_set_proportion, output_train_fp, output_test_fp):
    for index in range(0, int(len(word_id_data) * train_set_proportion)):
        output_train_fp.write(word_id_data[index])
    for index in range(int(len(word_id_data) * train_set_proportion), \
            int(len(word_id_data))):
        output_test_fp.write(word_id_data[index])
    return

def main():
    if len(sys.argv) < 4:
        print "Invalid Command. Usage: python " + sys.argv[0] + \
                " InputWordIDDataPath OutputWordIDTrainData OutputWordIDTestData [TrainTestProportion]"
        return

    # Train/Test sets Proportion Param Setting.
    train_set_proportion = 0
    test_set_proportion = 1
    if len(sys.argv) >= 5:
        num_list = [int(num) for num in sys.argv[4].strip().split(':')]
        if len(num_list) == 2:
            train_set_proportion = num_list[0] * 1.0 / sum(num_list)
            test_set_proportion = num_list[1] * 1.0 / sum(num_list)
    print "Train:Test sets Proportion: %d:%d" % (train_set_proportion / test_set_proportion, 1)

    # Shuffle.
    word_id_data_path = sys.argv[1]
    shuffled_word_id_data = Shuffle(word_id_data_path)

    total_num=len(shuffled_word_id_data)

    num=int(sys.argv[4])
    #test_set_proportion=float(float(int(num))/total_num)
    #train_set_proportion=1-test_set_proportion
    print "begin"
    #print num
    print total_num

    print test_set_proportion
    print train_set_proportion
    if train_set_proportion<0:
        test_set_proportion=1.0
        train_set_proportion=0.0
    if num>total_num:
        num=total_num
    test_set_proportion=float(num)/total_num
    train_set_proportion=1-test_set_proportion
    print test_set_proportion
    print train_set_proportion

    # Split Train Test sets and Output.
    output_train_fp = open(sys.argv[2], 'w')
    output_test_fp = open(sys.argv[3], 'w')
    SplitWordIDData2TrainTest(shuffled_word_id_data, train_set_proportion,
            test_set_proportion, output_train_fp, output_test_fp)

    return

if  __name__ == "__main__":
    main()

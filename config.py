#coding: utf8
from __future__ import print_function
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-e", "--eval", help="eval set file path", default="crf_data/eval.crf", type=str)
parser.add_argument("-t", "--test", help="test set file path", default="crf_data/test.crf", type=str)
parser.add_argument("-s", "--summary", help="summary file path", default="tmp/summary.dat", type=str)
parser.add_argument("-m", "--mode", help="analysis mode [all,both,eval,test]", default="all", type=str)
parser.add_argument("-c", "--collapse_type", help="collapse mode [all,ground,predict]", default="all", type=str)
parser.add_argument("-i", "--input", help="input crf file path", default="crf_data/test.raw.crf", type=str)

args = parser.parse_args()
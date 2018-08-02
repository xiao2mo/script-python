#coding: utf8
"""
合并多个字典，
对于有歧义的term（一个term可能有多个NER的义项）, 进行合并。
比如
成都 \t LOC.ADMIN
成都 \t ENT.MUSIC    ===>    成都 \t LOC.ADMIN \t ENT.MUSIC

示例:
python script/build_dict.py -i dict/LOC.HSCAAT.dict,dict/ent.dict,dict/product.dict -o dict/NER.dict
"""
from __future__ import print_function
import subprocess
import argparse
import sys
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input multiple dict, split by \",\"", default=None, type=str)
parser.add_argument("-o", "--output", help="output single dict ", default=None, type=str)
args = parser.parse_args()

ner2_order = {
    'ADMIN' : 0,
    'ADDR' : 1,
    'CATER' : 2,
    'HOTEL' : 3,
    'SCENE' : 4,
    'STATION' : 5,
    'LOC_TAG' : 6,
    'LOC_OTHER' : 7,
    'PROD_BRAND' : 8,
    'PROD_NAME' : 9,
    'PROD_TAG' : 10,
    'PROD_OTHER' : 11,
    'ENT_OTHER' : 12,
    'SCHOOL' : 13,
    'HOSPITAL' : 14,
    'PERSON_NAME' : 15,
    'GOV' : 16,
    'TV' : 17,
    'FILM' : 18,
    'MUSIC' : 19,
    'COMIC' : 20,
    'ORG_OTHER' : 21,
    'FLIGHT_NUM' : 22,
    'TRAIN_NUM' : 23,
    'BUS_NUM' : 24,
    'EXPRESS_CODE' : 25,
    'ZIP_CODE' : 26,
    'NUM_OTHER' : 27,
    'DATE' : 28,
    'CLOCK' : 29,
    'DAY' : 30,
    'TIME_OTHER' : 31,
    'OTHER' : 10000
    }

def tag_comp(o1, o2):
    o1_toks = o1.split('.')
    o2_toks = o2.split('.')
    if len(o1_toks) == 2:
        o1_tag = o1_toks[1]
    else:
        o1_tag = o1_toks[-1]
    if len(o2_toks) == 2:
        o2_tag = o2_toks[1]
    else:
        o2_tag = o2_toks[-1]
    o1_order = ner2_order.get(o1_tag, 10000)
    o2_order = ner2_order.get(o2_tag, 10000)
    if o1_order < o2_order:
        return -1
    elif o1_order > o2_order:
        return 1
    else:
        return 0

def combine_multi_sense(l):
    term = l[0][0]
    tags = [t[1] for t in l]
    # duplicate
    tags = list(set(tags))
    tags = sorted(tags, cmp=tag_comp)
    out_s = '{}\t{}'.format(term, '\t'.join(tags))
    return out_s

def data_itr(fname):
    prv = None
    cur = None
    out_l = []
    with open(fname, 'r') as fin:
        for line in fin:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue
            toks = line.split('\t')
            if len(toks) < 2:
                continue
            cur = toks[0]
            if prv is None:
                prv = cur
                out_l.append(toks)
                continue

            if prv == cur:
                out_l.append(toks)
            else:
                if len(out_l) > 0:
                    out_s = combine_multi_sense(out_l)
                    yield out_s
                prv = cur
                out_l = [toks, ]
    if len(out_l) > 0:
        out_s = combine_multi_sense(out_l)
        yield out_s
        out_l = []

def main():
    ordered_fname = 'tmp.dat'
    forder = open(ordered_fname, 'w')
    # concat and sort
    cat_cmd = 'cat ' + ' '.join(args.input.split(','))
    proc_cat = subprocess.Popen([cat_cmd], shell=True, stdout=forder)
    proc_cat.wait()
    forder.close()
    print("preprocess finished...")
    sys.stdout.flush()

    fout = open(args.output, 'w')
    for s in data_itr(ordered_fname):
        fout.write(s + '\n')
    fout.close()

if __name__ == '__main__':
    main()

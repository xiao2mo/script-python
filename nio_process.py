#coding: utf8
"""
将nio的数据加工成trio的label数据格式(NER的部分使用[NOR]xxx[NER_TYPE1->NER_TYPE2]).
"""
from __future__ import print_function
import sys
import re
tag_pt = re.compile(r'[BI]-(.*?)$')

trans = {}

def load_trans(fname):
    global trans
    with open(fname, 'r') as fin:
        for line in fin:
            toks = line.rstrip('\n').split(' ')
            assert(len(toks) == 2)
            trans[toks[0]] = toks[1]
    return

def main():
    load_trans('dict/nio2trio.dict')
    for line in open(sys.argv[1], 'r'):
        line = line.rstrip('\n')
        toks = line.split('\t')

        if len(toks) != 2:
            sys.stderr.write("format error [{}]".format(line))
            sys.exit(-1)
        term_fea, tags = toks
        tags = tags.split(' ')
        sub_toks = term_fea.split(' ')
        n_len = len(sub_toks)
        terms, feas = sub_toks[:n_len / 2], sub_toks[n_len/2 + 1:]
        if len(terms) != len(tags):
            sys.stderr.write("format error. terms [{}] len {}, tags [{}] len {}\n".format(' '.join(terms), len(terms), ' '.join(tags), len(tags)))
            continue
        start = False
        l = []
        sub_terms = []
        prv_tag = None
        term_tags = zip(terms, tags)
        i = 0
        while i < len(term_tags):
            term, tag = term_tags[i]
            tag_pos = 'O'
            m = tag_pt.search(tag)
            if m is None:
                tag = 'O'
            else:
                tag_pos = tag[0]
                tag = m.group(1)

            if prv_tag is None:
                prv_tag = tag
                if tag_pos == 'O':
                    l.append(term)
                else:
                    sub_terms.append(term)
                i += 1
                continue

            if tag == prv_tag:
                if tag_pos in ['O', 'I']:
                    sub_terms.append(term)
                elif tag_pos in ['B']:
                    tgt_tag = trans.get(prv_tag, 'O')
                    if tgt_tag != 'O':
                        s = '[NOR]{}[{}]'.format(''.join(sub_terms), tgt_tag)
                    else:
                        s = ''.join(sub_terms)
                    l.append(s)
                    sub_terms = [term,]
                    prv_tag = tag
            else:
                tgt_tag = trans.get(prv_tag, 'O')
                if tgt_tag != 'O':
                    s = '[NOR]{}[{}]'.format(''.join(sub_terms), tgt_tag)
                else:
                    s = ''.join(sub_terms)
                l.append(s)
                sub_terms = [term,]
                prv_tag = tag
            i += 1
        if len(sub_terms) > 0:
            tgt_tag = trans.get(prv_tag, 'O')
            if tgt_tag != 'O':
                s = '[NOR]{}[{}]'.format(''.join(sub_terms), tgt_tag)
            else:
                s = ''.join(sub_terms)
            l.append(s)
        out_s = ''.join(l)
        print(out_s)

if __name__ == '__main__':
    main()
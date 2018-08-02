# coding: utf8
'''
对于character-level的training crf格式的数据，抽取NER标签.
数据格式一般为
char fea NER_TAG
'''
from __future__ import print_function
from config import args

trans = {
    "O": "O",
    "SL": "B-LOC",
    "ML": "I-LOC",
    "EL": "E-LOC",
    "SO": "B-ORG",
    "MO": "I-ORG",
    "EO": "E-ORG",
    "L": "B-LOC"
}


def extract_analysis(l):
    l = [s.split(' ') for s in l]
    l = [t for t in l if len(t) == 3]
    ws, gs = [t[0] for t in l], [t[2] for t in l]
    ws, gs = ws[1:-1], gs[1:-1], ps[1:-1]
    gs = [trans[tag] for tag in gs]

    ne_g = extract_entities(ws, gs)
    # print(ne_g)
    ws = ''.join(ws)
    gs = ''.join(gs)
    return ws, gs, ne_g


def extract_entities(ws, tags):
    tags = [trans[tag] for tag in tags]
    ne = []
    tmp_l = []
    start = -1
    prv_tag_type = None
    for i, (w, tag) in enumerate(zip(ws, tags)):
        if tag == 'O':
            tag_type = 'O'
            if len(tmp_l) > 0:
                t = (''.join(tmp_l), prv_tag_type, start, len(tmp_l))
                ne.append(t)
                tmp_l = []
                prv_tag_type = tag_type
            else:
                pass
        else:
            tag_type = tag[2:]
        if prv_tag_type is None:
            prv_tag_type = tag_type

        if tag.startswith('B-') or ((tag.startswith('I-') or tag.startswith('E-')) and prv_tag_type != tag_type):
            if len(tmp_l) > 0:
                t = (''.join(tmp_l), prv_tag_type, start, len(tmp_l))
                ne.append(t)
                tmp_l = []
                prv_tag_type = tag_type
            start = i
            tmp_l.append(w)
            prv_tag_type = tag_type
        elif tag != 'O':
            tmp_l.append(w)
    if len(tmp_l) > 0:
        t = (''.join(tmp_l), prv_tag_type, start, len(tmp_l))
        ne.append(t)
    return ne


def sent_iter(fname):
    l = []
    with open(fname, 'r') as fin:
        for line in fin:
            line = line.rstrip('\n')
            if len(line) < 1:
                yield extract_analysis(l)
                l = []
                continue
            else:
                l.append(line)


def test():
    '''
    <S> O O
    请 O O
    勿 O O
    转 O O
    发 O O
    【 O O
    腾 B-ORG O
    讯 I-ORG O
    科 I-ORG O
    技 E-ORG O
    】 O O
    <E> O O
    '''
    ws = ['请', '勿', '转', '发', '【', '腾', '讯', '科', '技', '】']
    gs = ['O', 'O', 'O', 'O', 'O', 'B-ORG', 'I-ORG', 'I-ORG', 'E-ORG', 'O']
    assert (len(ws) == len(gs))
    ne_g = extract_entities(ws, gs)
    assert (len(ne_g) == 1)
    w, ne, start = ne_g[0]
    assert (w == '腾讯科技')
    assert (ne == 'ORG')
    assert (start == 5)

    ws = ['北', '京', '转', '发', '【', '腾', '讯', '科', '技', '新', '浪', '】']
    gs = ['B-LOC', 'E-LOC', 'O', 'O', 'O', 'B-ORG', 'I-ORG', 'I-ORG', 'E-ORG', 'B-ORG', 'I-ORG', 'O']
    assert (len(ws) == len(gs))
    ne_g = extract_entities(ws, gs)
    assert (len(ne_g) == 3)
    assert (ne_g[0] == ('北京', 'LOC', 0))
    assert (ne_g[1] == ('腾讯科技', 'ORG', 5))
    assert (ne_g[2] == ('新浪', 'ORG', 9))
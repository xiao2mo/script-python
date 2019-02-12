#coding: utf8
import re
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", help="mode [rm|stats|add|modify]", default="rm", type=str)
parser.add_argument("-i", "--input", help="input file", default="tmp/app/zhidao.label", type=str)
parser.add_argument("-o", "--output", help="output file", default="tmp/app/zhidao.label.1", type=str)
parser.add_argument("-t", "--term", help="term file", default=None, type=str)
parser.add_argument("-tag", "--tag", help="tag list, separated by comma", default=None, type=str)
args = parser.parse_args()

suffixdict=set()
for iterm in open("all.suffix","r"):
    suffix=iterm.rstrip("\n")
    suffixdict.add(suffix)
def rm_routine():
    term_d = {}
    if args.term is not None:
        with open(args.term, 'r') as fin:
            for line in fin:
                line = line.rstrip('\n')
                toks = line.split('\t')
                term, cnt = toks[:2]
                term_d[term] = cnt
    all_tag = False
    if args.tag == "all":
        all_tag = True
    else:
        tag_d = {}
        if args.tag is not None:
            for tag in args.tag.split(','):
                tag_d[tag] = 1

    pt = re.compile(r'\[NOR\]([^[]+)\[([^]]+)\]')
    d = {}
    fout = open(args.output, 'w')
    fout2=open("intersec.ner","w")
    count=0
    with open(args.input, 'r') as fin:
        for newline in fin:
            line = newline.rstrip('\n')
            s = line
            out_l = []
            prv_end = 0
            slen = len(s)
            for m in pt.finditer(s):
                beg, end = m.span()
                term, tag = m.group(1), m.group(2)
                out_l.append(s[prv_end:beg])
                if all_tag:
                    for suffix in suffixdict:
                        if term.endswith(suffix):
                            fout2.write(newline)
                            continue 
                        else:
                            out_l.append(term)
                else:
                    if tag_d.has_key(tag):
                        out_l.append(term)
                    elif term_d.has_key(term):
                        out_l.append(term)
                    else:
                        out_l.append(m.group(0))
                prv_end = end
            if prv_end < slen:
                out_l.append(s[prv_end:])
            out_s = ''.join(out_l)
            fout.write(out_s + '\n')
            if count%500==0:
                print("now we are processing line : ",count)
            count+=1
    return

def stats_routine():
    pt = re.compile(r'\[NOR\]([^[]+)\[([^]]+)\]')
    d = {}
    fout = open(args.output, 'w')
    with open(args.input, 'r') as fin:
        for line in fin:
            line = line.rstrip('\n')
            for m in pt.finditer(line):
                term, tag = m.group(1), m.group(2)
                d[term] = d.get(term, 0) + 1
    l = sorted(d.items(), key=lambda x:x[1], reverse=True)
    for term,cnt in l:
        #print('{}\t{}'.format(term,cnt))
        fout.write('{}\t{}\n'.format(term,cnt))
    fout.close()

def add_routine():
    pass

def modify_routine():
    pass

def main():
    if args.mode == "rm":
        rm_routine()
    elif args.mode == "stats":
        stats_routine()
    elif args.mode == "add":
        add_routine()
    elif args.mode == "modify":
        modify_routine()
    else:
        raise ValueError("mode not recognized {}".format(args.mode))

if __name__ == '__main__':
    main()

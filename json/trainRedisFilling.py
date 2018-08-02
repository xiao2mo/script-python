#coding: utf8
from __future__ import print_function
import json
import redis
import sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--mode", help="process mode[crawl|write|dump] ", default="write")
parser.add_argument("-f", "--file", help="url list|db file")
#parser.add_argument("-host", "--redis_host", help="redis host", default="10.0.2.204", type = str)
parser.add_argument("-host", "--redis_host", help="redis host", default="10.31.77.158", type = str)
#parser.add_argument("-host", "--redis_host", help="redis host", default="10.0.2.17", type = str)
parser.add_argument("-p", "--redis_port", help="redis port", default=6379, type=int)
parser.add_argument("-pwd", "--password", help="redis password", default="1234567Myc", type=str)
# parser.add_argument("-pwd", "--password", help="redis password", default="", type=str)
parser.add_argument("-prefix", "--prefix", help="redis key prefix", default="TR", type=str)
parser.add_argument("-pattern", "--pattern", help="redis key pattern", default="TR_*", type=str)
args = parser.parse_args()

URL_PRE = "https://train.qunar.com/list_num.htm?fromStation="

def format_kv(prefix, id, s_from, s_to, d_time, a_time, mile):
    d = {
        "resultcode" : "200",
        "reason" : "Successed",
        "result" : {
             "train_info" : {
                 "name" : id,
                 "start" : s_from,
                 "end" : s_to,
                 "starttime" : d_time,
                 "endtime" : a_time,
                 "mileage" : "",
                 "route":mile
            }
        }
    }
    s_json = json.dumps(d)
    k = prefix + "_" + id
    return k, s_json

def write_db_routine(fname, redis_host, redis_port, passwd):
    r = redis.Redis(host = redis_host, port = redis_port, password=passwd)
    count=0
    with open(fname, 'r') as fin:
        for line in fin:

            if count%100==0:
                print("now we are processing %d line"%count)
            count+=1
            line = line.rstrip('\n')
            toks = line.split('\t')
            if len(toks) != 6:
                sys.stderr.write('format error {}\n'.format(line))
                continue
            id, s_from, s_to, d_time, a_time,mile = toks[:6]
            k,v = format_kv(args.prefix, id, s_from, s_to, d_time, a_time,mile)
            if "Z2" in k:
                print(k)
            r.set(k, v)
    return

def dump_data(key_pattern, redis_host, redis_port, passwd):
    r = redis.Redis(host = redis_host, port = redis_port, password=passwd)
    l = r.keys(key_pattern)
    for k in l:
        v = r.get(k)
        print('{}\t{}'.format(k, v))

def key_test(key_pattern, redis_host, redis_port, passwd):
    r = redis.Redis(host = redis_host, port = redis_port, password=passwd)
    l = r.keys(key_pattern)
    for k in l:
        v = r.get(k)
        if k=="TR_Z2":
            #print(k) 
            print('{}\t{}'.format(k, v))


if __name__ == '__main__':
    if args.mode == "crawl":
        crawl_train_info(args.file)
    elif args.mode == "write":
        write_db_routine(args.file, args.redis_host, args.redis_port, args.password)
    elif args.mode == "test":
        key_test(args.pattern, args.redis_host, args.redis_port, args.password)
    elif args.mode == "dump":
        dump_data(args.pattern, args.redis_host, args.redis_port, args.password)
    else:
        sys.exit(-1)
    print('SUCCESS')

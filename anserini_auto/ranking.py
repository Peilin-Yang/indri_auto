from __future__ import print_function, absolute_import, division

import os, sys
import time
import subprocess
import argparse

binary = 'target/appassembler/bin/SearchWebCollection'
topics_root = 'src/main/resources/topics-and-qrels'
indexes = {
    'lucene-index.cw09b.cnt.1': ('Webxml', ['topics.web.51-200.txt']),
    'lucene-index.cw09.cnt.1': ('Webxml', ['topics.web.51-200.txt']),
    'lucene-index.cw12b13.cnt.1': ('Webxml', ['topics.web.201-300.txt']),
    'lucene-index.cw12.cnt.1': ('Webxml', ['topics.web.201-300.txt']),
}
"""
indexes = {
    'disk12': ('Trec', 'topics.disk12.all.txt'),
    'disk45': ('Trec', 'topics.robust04.301-450.601-700.txt'),
    'AQUAINT': ('Trec', 'topics.robust05.txt'),
    'wt2g': ('Trec', 'topics.401-450.txt'),
    'wt10g': ('Trec', 'topics.451-550.txt'),
    'gov2-corpus': ('Trec', 'topics.gov2.all.txt'),
}
"""
#models = ['bm25', 'ql', 'pl2', 'f2exp', 'spl']
models = ['bm25']

def mkdir(path):
    abspath = os.path.abspath(path)
    if not os.path.exists(abspath):
        os.makedirs(abspath)
    elif os.path.isdir(abspath): 
        print('Path %s exists ... we are fine..' % abspath)        
    else:
        raise('Path Error: %s' % abspath)

def collect_all_index(path='index'):
    all_indexes = {}
    for folder in os.listdir(path):
        if not os.path.isdir(os.path.join(path, folder)):
            continue
        all_indexes[folder] = os.path.join(path, folder)

    return all_indexes

def batch_rank(args, iter_n=3):
    mkdir(args.output_root)
    mkdir(args.log_root)
    all_indexes = collect_all_index(args.index_root)

    for model in models:
        for i in range(iter_n):
            for index, path in all_indexes.items():
                print(index, path)
                #collection = index.split('.')[0]
                collection = index
                if collection not in indexes:
                    continue
                for topic in indexes[collection][1]:
                  binary_fp = os.path.join(args.anserini_root, binary)
                  command = [binary_fp]
                  command.extend(['-topicreader', indexes[collection][0]])
                  command.extend(['-index', path])
                  command.extend(['-%s'%model])
                  command.extend(['-topics', os.path.join(args.anserini_root, topics_root, topic)])
                  index_base = os.path.basename(path)
                  command.extend(['-output', os.path.join(args.output_root, index_base+'.'+topic+'.'+model)])

                  log_path = os.path.join(args.log_root, index_base+'.'+topic+'.'+model+'.%d'%i)
                  log_fp = open(log_path, "w")
                  subprocess.call(command, stdout=log_fp)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--anserini_root', 
        type=str, 
        default='',
        required=True
    )
    parser.add_argument(
        '--index_root', 
        type=str, 
        default='',
        required=True
    )
    parser.add_argument(
        '--output_root', 
        type=str, 
        default='',
        help='root path for the ranking list files'
    )
    parser.add_argument(
        '--log_root', 
        type=str, 
        default='',
        help='root path for log files'
    )
    return parser.parse_args()

if __name__ == '__main__':

    args = parse_arguments()
    #print(args)
    batch_rank(args)

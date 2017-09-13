from __future__ import print_function, absolute_import, division

import os, sys
import time
import datetime
import subprocess
import argparse

binary = 'IndriRunQuery'
models = ['okapi', 'dir']

def mkdir(path):
    abspath = os.path.abspath(path)
    if not os.path.exists(abspath):
        os.makedirs(abspath)
    elif os.path.isdir(abspath): 
        print('Path %s exists ... we are fine..' % abspath)        
    else:
        raise('Path Error: %s' % abspath)

def batch_rank(args, iter_n=3):
    mkdir(args.output_root)
    mkdir(args.log_root)

    for i in range(iter_n):
        for topic_fn in os.listdir(args.topics_root): 
            for model in models:
                command = [binary, os.path.join(args.topics_root, topic_fn), '-index=%s' % os.path.abspath(os.path.join(args.index_root, topic_fn)), '-rule=method:%s' % model]
                log_path = os.path.join(args.log_root, topic_fn+'.'+model+'.%d'%i)
                res_fp = open(os.path.join(args.output_root, topic_fn+'.'+model), "w")
                start_time = time.time()
                subprocess.call(command, stdout=res_fp)
                elapsed_time = time.time() - start_time
                #print(command, log_path, str(datetime.timedelta(round(elapsed_time, 0))))
                with open(log_path, 'w') as f:
                    f.write(str(datetime.timedelta(seconds=round(elapsed_time, 0))))

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--topics_root', 
        type=str, 
        default='queries',
    )
    parser.add_argument(
        '--index_root', 
        type=str, 
        default='indexes',
    )
    parser.add_argument(
        '--output_root', 
        type=str, 
        default='ranking',
        help='root path for the ranking list files'
    )
    parser.add_argument(
        '--log_root', 
        type=str, 
        default='ranking.logs',
        help='root path for log files'
    )
    return parser.parse_args()

if __name__ == '__main__':

    args = parse_arguments()
    #print(args)
    batch_rank(args)

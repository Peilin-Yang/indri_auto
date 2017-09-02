from __future__ import print_function, absolute_import, division

import os, sys
import shutil
import datetime
import subprocess
import argparse

binary = 'IndriBuildIndex'

def mkdir(path):
    abspath = os.path.abspath(path)
    if not os.path.exists(abspath):
        print('Creating folder: %s' % abspath)
        os.makedirs(abspath)
    elif os.path.isdir(abspath): 
        #print('Path %s exists ... we are fine..' % abspath)
        pass
    else:
        raise('Path Error: %s' % abspath)

def get_name_from_path(path):
    """
    Get the corpus name from its path:
    (1) if it is /a/b/c/ then return c
    (2) if it is /a/b/c then it is simpler, we also return c
    """
    if os.path.basename(path):
        return os.path.basename(path)
    else:
        return os.path.basename(path[:-1])

def build(args):
    mkdir(args.log_root)
    mkdir(args.index_root)
    corpus_name = get_name_from_path(args.corpus_root)
    output_index_path = os.path.join(args.index_root, corpus_name)
    if os.path.isfile(output_index_path):
        os.remove(output_index_path)
    if os.path.isdir(output_index_path):
        shutil.rmtree(output_index_path)
    binary_fp = os.path.join(args.indri_root, binary)
    command = [binary_fp, args.build_para_fn]
    command.append( '-index=%s' % (os.path.join(args.index_root, corpus_name)) )
    command.append( '-corpus.path=%s' % (args.corpus_root) )
    command.append( '-corpus.class=%s' % (args.corpus_type) )
    command.append( '-memory=%sG' % (args.mem_gb) )
    
    i = 1
    log_path = corpus_name
    while True:
        if os.path.exists( os.path.join(args.log_root, log_path+'.%d' % i) ):
            i += 1
        else:
            log_path += '.%d' % i
            break
    log_path = os.path.join(args.log_root, log_path)
    print('%s | Running: %s > %s' % (datetime.datetime.now(), ' '.join(command), log_path))
    log_fp = open(log_path, "w")
    subprocess.call(command, stdout=log_fp)

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--indri_root', 
        type=str, 
        default='',
        required=True
    )
    parser.add_argument(
        '--build_para_fn', 
        type=str, 
        default='',
        required=True,
        help='the parameter fn for building the index'
    )
    parser.add_argument(
        '--corpus_type', 
        type=str, 
        choices=['trectext', 'trecweb', 'warc'],
        default='trecweb',
        required=True,
        help='type of the collection'
    )
    parser.add_argument(
        '--mem_gb', 
        type=str, 
        default='2',
        help='memory used for the indexing, default 2GB'
    )
    parser.add_argument(
        '--log_root', 
        type=str, 
        default='',
        help='root path for log files'
    )
    parser.add_argument(
        '--corpus_root', 
        type=str, 
        default='',
        help=' the corpus folder'
    )
    parser.add_argument(
        '--index_root', 
        type=str, 
        default='',
        help='folder path of the output index'
    )
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_arguments()
    #print(args)
    build(args)

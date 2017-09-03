from __future__ import print_function, absolute_import, division

import os, sys
import shutil
import datetime
import subprocess
import argparse

binary = 'IndexCollection'

def mkdir(path):
    abspath = os.path.abspath(path)
    if not os.path.exists(abspath):
        os.makedirs(abspath)
    elif os.path.isdir(abspath): 
        print('Path %s exists ... we are fine..' % abspath)        
    else:
        raise('Path Error: %s' % abspath)

def build(args):
    mkdir(args.output_root)
    mkdir(args.log_root)

    binary_fp = os.path.join(args.anserini_root, binary)
    command = [binary_fp]
    command.extend(['-input', args.corpus_root])
    command.extend(['-collection', args.ctype+'Collection'])
    command.extend(['-generator', 'LuceneDocumentGenerator'])
    command.extend(['-threads', args.threads])

    if os.path.basename(args.corpus_root):
        index_path = os.path.basename(args.corpus_root)
    else:
        index_path = os.path.basename(args.corpus_root[:-1])
    
    if args.pos:
        command.append('-storePositions')
        index_path += '.pos'
    if args.docvec:
        command.append('-storeDocvectors')
        index_path += '.docvec'
    if args.raw:
        command.append('-storeRawDocs')
        index_path += '.rawdocs'
    if args.merge:
        command.append('-optimize')
        index_path += '.merge'

    log_path = index_path + '.threads%s' % args.threads
    i = 1
    while True:
        if os.path.exists( os.path.join(args.log_root, log_path+'.%d' % i) ):
            i += 1
        else:
            log_path += '.%d' % i
            break

    log_path = os.path.join(args.log_root, log_path)
    index_path = os.path.join(args.output_root, index_path)
    if os.path.isfile(index_path):
        os.remove(index_path)
    if os.path.isdir(index_path):
        shutil.rmtree(index_path)

    command.extend(['-index', index_path])
    print('%s | Running: %s > %s' % (datetime.datetime.now(), ' '.join(command), log_path))

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
        '--corpus_root', 
        type=str, 
        default='',
        required=True
    )
    parser.add_argument(
        '--ctype', 
        choices=['Trec', 'Wt', 'Gov2', 'TrecCore', 'CW09', 'CW12'],
        required=True,
        help='Collection type'
    )
    parser.add_argument(
        '--output_root', 
        type=str, 
        default='',
        help='root path for the output index'
    )
    parser.add_argument(
        '--threads', 
        type=str, 
        default='16'
    )
    parser.add_argument(
        '--pos', 
        action='store_true',
        help='whether to store the positions'
    )
    parser.add_argument(
        '--docvec', 
        action='store_true', 
        help='whether to store the document vectors'
    )
    parser.add_argument(
        '--raw', 
        action='store_true',
        help='whether to store the raw documents'
    )
    parser.add_argument(
        '--merge', 
        action='store_true', 
        help='whether to merge the index to one segment'
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
    build(args)

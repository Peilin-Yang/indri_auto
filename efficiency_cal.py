from __future__ import print_function, absolute_import, division

import os, sys
import datetime
import math
import argparse

def collect_all(log_root):
    all_log_files = {}
    for fn in os.listdir(log_root):
        k = '.'.join(fn.split('.')[:-1]) # we should have multiple logs for each run
        if k not in all_log_files:
            all_log_files[k] = []	
        all_log_files[k].append(os.path.join(log_root, fn))

    return all_log_files

def get_duration(fn, _type='index'):
    try:
        with open(fn) as f:
            last_line = f.readlines()[-1]
        t = last_line.split(':')
        if _type == 'index':
            return int(t[0])*60 + int(t[1])
        elif _type == 'ranking':
            return int(t[0])*3600 + int(t[1])*60 + int(t[2])
    except:
        print('Something wrong with log file:%s' % fn)
        return -1
 
def mean(data):
    """Return the sample arithmetic mean of data."""
    n = len(data)
    if n < 1:
        raise ValueError('mean requires at least one data point')
    return sum(data)/float(n) # in Python 2 use sum(data)/float(n)

def _ss(data):
    """Return sum of square deviations of sequence data."""
    c = mean(data)
    ss = sum((x-c)**2 for x in data)
    return ss

def pstdev(data):
    """Calculates the population standard deviation."""
    n = len(data)
    if n < 2:
        return 0
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5

def cal_efficiency(args):
    all_logs = collect_all(args.log_root)
    all_stats = {}
    for k in all_logs:
        all_stats[k] = []
        for fn in all_logs[k]:
            duration = get_duration(fn, args.type)
            if duration > 0:
                all_stats[k].append(duration)
    if args.type == 'index':
        print('collection', 'iter_times', 'mean', 'std')
        for collection in sorted(all_stats):
            print(collection, len(all_stats[collection]), '%s'%str(datetime.timedelta(seconds=round(mean(all_stats[collection]), 0))), '%.1f'%pstdev(all_stats[collection]))
    if args.type == 'ranking':
        final_stats = {}
        for k in all_stats:
            collection, model = k.split('.')
            if collection not in final_stats:
                final_stats[collection] = {}
            if model not in final_stats[collection]:
                final_stats[collection][model] = all_stats[k]
        for collection in sorted(final_stats):
            for model in sorted(final_stats[collection]):
                    l = final_stats[collection][model]
                    print(collection, model, len(l), '%s'%str(datetime.timedelta(seconds=round(mean(l), 0))), '%.1f'%pstdev(l))
                     

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--log_root', 
        type=str, 
        default='',
        required=True
    )
    parser.add_argument(
        '--type', 
        choices=['index', 'ranking'],
        required=True,
        help='log type'
    )
    return parser.parse_args()

if __name__ == '__main__':

    args = parse_arguments()
    #print(args)
    cal_efficiency(args)

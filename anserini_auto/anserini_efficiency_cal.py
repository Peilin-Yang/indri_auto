from __future__ import print_function, absolute_import, division

import os, sys
import re 
import math
import datetime
import argparse

def collect_all(log_root):
    all_log_files = {}
    for fn in os.listdir(log_root):
        k = '.'.join(fn.split('.')[:-1]) # we should have multiple logs for each run
        if k not in all_log_files:
            all_log_files[k] = []	
        all_log_files[k].append(os.path.join(log_root, fn))

    return all_log_files

def get_duration(fn):
    try:
        with open(fn) as f:
            last_line = f.readlines()[-1]
        t = last_line.split()[-1].split(':')
        return int(t[0]) * 3600 + int(t[1]) * 60 + int(t[2])
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
        # raise ValueError('variance requires at least two data points')
    ss = _ss(data)
    pvar = ss/n # the population variance
    return pvar**0.5

def cal_efficiency(args):
    all_logs = collect_all(args.log_root)
    all_stats = {}
    for k in all_logs:
        all_stats[k] = []
        for fn in all_logs[k]:
            duration = get_duration(fn)
            if duration > 0:
                all_stats[k].append(duration)
    final_stats = {}
    if args.type == 'index':
        for k in all_stats:
            collection = k.split('.')[0]
            if collection not in final_stats:
                final_stats[collection] = {}
            if 'merge' in k:
                merge_type = 'merge'
            else:
                merge_type = 'unmerge'
            option = k.replace(collection+'.', '').replace('merge.', '')
            threads = option[-2:]
            if threads != '44':
                continue
            option = re.sub(r'\.*threads\d+', '', option)
            if option not in final_stats[collection]:
                final_stats[collection][option] = {}
            if merge_type not in final_stats[collection][option]:
                final_stats[collection][option][merge_type] = {}
            if threads not in final_stats[collection][option][merge_type]:
                final_stats[collection][option][merge_type][threads] = all_stats[k]
        print('collection', 'option', 'merge', 'threads', 'iter_times', 'mean', 'std')
        for collection in sorted(final_stats):
            for option in sorted(final_stats[collection]):
                for merge_type in sorted(final_stats[collection][option]):
                    _min = 9e8 
                    cur_res = []
                    for threads in sorted(final_stats[collection][option][merge_type]):
                        l = final_stats[collection][option][merge_type][threads]
                        avg = mean(l)
                        if avg < _min:
                            _min = avg
                        cur_res.append((collection, option, merge_type, threads, len(l), avg, pstdev(l)))
                    for ele in cur_res:
                        if math.fabs(_min - ele[5]) < 1e-6:
                            print(ele[0], ele[1], ele[2], ele[3], ele[4], '%s'%str(datetime.timedelta(seconds=round(ele[5], 0))), '%.1f'%ele[6])                 
                        else:
                            print(ele[0], ele[1], ele[2], ele[3], ele[4], '%s'%str(datetime.timedelta(seconds=ele[5])), '%.1f'%ele[6])                 
    if args.type == 'ranking':
        for k in all_stats:
            ksplits = k.split('.')
            collection = ksplits[0]
            if collection not in final_stats:
                final_stats[collection] = {}
            if 'merge' in k:
                merge_type = 'merge'
            else:
                merge_type = 'unmerge'
            option = k.replace(collection+'.', '').replace('merge.', '')
            option = re.sub(r'\.*threads\d+', '', option)
            model = option.split('.')[-1]
            option = option.replace('.'+model, '')
            if option not in final_stats[collection]:
                final_stats[collection][option] = {}
            if model not in final_stats[collection][option]:
                final_stats[collection][option][model] = {}
            if merge_type not in final_stats[collection][option][model]:
                final_stats[collection][option][model][merge_type] = all_stats[k]
        for collection in sorted(final_stats):
            for option in sorted(final_stats[collection]):
                for model in sorted(final_stats[collection][option]):
                    for merge_type in sorted(final_stats[collection][option][model]):
                        l = final_stats[collection][option][model][merge_type]
                        print(collection, option, merge_type, model, len(l), '%s'%str(datetime.timedelta(seconds=round(mean(l), 0))), '%.1f'%pstdev(l))
                     

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

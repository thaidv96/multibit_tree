import pandas as pd
import numpy as np
from datetime import datetime
from multiprocessing import Pool, cpu_count
import sys
from collections import Counter
import pickle
import re
path = sys.argv[1]
chunksize = int(sys.argv[2])
condition = sys.argv[3]

dfs = pd.read_csv(path, chunksize=chunksize)
start_time = datetime.now()
res = Counter()
counted = 0
start_time = datetime.now()
num_records = 0


def check_in_condition(conds, values):
    res = True
    for cond in conds:
        res &= (cond in values)
    return res


def check_not_in_condition(conds, values):
    res = True
    for cond in conds:
        res &= (cond not in values)
    return res


def func(df, condition):
    true_idx = [i.split() for i in df.Fingerprint.values]

    must_have = re.findall(r'~(\d+)', condition)
    not_have = re.findall(r'!(\d+)', condition)
    true_idx = [o for o in true_idx if (check_in_condition(
        must_have, o) & check_not_in_condition(not_have, o))]
    global num_records
    num_records += len(true_idx)
    true_idx = [i for o in true_idx for i in o]
    c = Counter(true_idx)

    global counted
    counted += 1
    current_time = datetime.now()
    print('running time:', current_time - start_time, 'completed', counted, 'estimated remaining:', (
        current_time-start_time)/counted * (120e6/chunksize - counted))
    return c


counters = []
for df in dfs:
    c = func(df, condition)
    counters.append(c)

with open(f'{condition}.pickle', 'wb') as handle:
    print("Start writing data")
    res = dict(sum(counters, Counter()))
    res['num_records'] = num_records
    pickle.dump(res, handle,
                protocol=pickle.HIGHEST_PROTOCOL)

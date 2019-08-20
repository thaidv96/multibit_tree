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


def func(df, condition):
    global counted
    counted += 1
    true_idx = df.Fingerprint.str.split()

    must_have = re.findall(r'~(\d+)', condition)
    not_have = re.findall(r'!(\d+)', condition)

    cond = np.ones_like(true_idx)
    for i in must_have:
        cond &= true_idx.apply(lambda x: i in x)
    for i in not_have:
        cond &= true_idx.apply(lambda x: i not in x)

    res = df[cond]

    current_time = datetime.now()
    print('running time:', current_time - start_time, 'completed', counted, 'estimated remaining:', (
        current_time-start_time)/counted * (120e6/chunksize - counted))
    return res


for i, df in enumerate(dfs):
    root_df = func(df, condition)
    if i == 0:
        root_df.to_csv(f"{condition}.csv")
    else:
        with open(f"{condition}.csv", 'a') as f:
            root_df.to_csv(f, header=False)

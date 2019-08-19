import pandas as pd
import numpy as np
from datetime import datetime
from multiprocessing import Pool, cpu_count
import sys
from collections import Counter
import pickle
path = sys.argv[1]
chunksize = int(sys.argv[2])
dfs = pd.read_csv(path, chunksize=chunksize)
start_time = datetime.now()
res = Counter()
counted = 0
start_time = datetime.now()


def func(df):
    true_idx = [i.split() for i in df.Fingerprint.values]
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
    c = func(df)
    counters.append(c)

with open('root_counter.pickle', 'wb') as handle:
    print("Start writing data")
    pickle.dump(sum(counters, Counter()), handle,
                protocol=pickle.HIGHEST_PROTOCOL)

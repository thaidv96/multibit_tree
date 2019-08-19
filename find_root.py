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
for i, df in enumerate(dfs):
    running_time = datetime.now()
    print("completed:", round(i*chunksize/120e4, 4), '%', 'estimated remaining:',
          (running_time-start_time)/((i + 1)*chunksize) * 120e6 - (running_time-start_time))
    true_idx = [i.split() for i in df.Fingerprint.values]
    true_idx = [i for o in true_idx for i in o]
    c = Counter(true_idx)
    res += c


with open('root_counter.pickle', 'wb') as handle:
    pickle.dump(res, handle, protocol=pickle.HIGHEST_PROTOCOL)

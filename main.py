import pandas as pd
import numpy as np
import sys
from multiprocessing import Pool, cpu_count
from tree import MultibitTree
import pickle

num_processes = cpu_count()-2


def convert_fingerprint(fingerprint):
    res = np.zeros(300)
    res[np.array(fingerprint).astype(int)] = 1
    return res.astype(bool)


def main():
    path = sys.argv[1]
    fingerprints = []
    chunksize = int(sys.argv[2])
    dfs = pd.read_csv(path, chunksize=chunksize)
    for df in dfs:
        sample_fingerprints = df.Fingerprint.str.split().values

        sample_fingerprints = [convert_fingerprint(
            i) for i in sample_fingerprints]

        fingerprints += sample_fingerprints
    fingerprints = np.array(fingerprints)
    with open(f'fingerprints.pickle', 'wb') as handle:
        pickle.dump(fingerprints, handle, protocol=pickle.HIGHEST_PROTOCOL)
    tree = MultibitTree(fingerprints, 'sample_tree')
    tree.build_tree()


if __name__ == '__main__':
    main()

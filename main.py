import pandas as pd
import numpy as np
import sys
from multiprocessing import Pool, cpu_count
from tree import MultibitTree
import pickle
import numpy as np
import glob
num_processes = cpu_count() - 2


def convert_fingerprint(fingerprints):

    res = np.zeros((len(fingerprints), 300))
    for idx, fingerprint in enumerate(fingerprints):
        res[idx, np.array(fingerprint).astype(int)] = 1
    return res.astype(bool)


def main():
    path = sys.argv[1]
    chunksize = int(sys.argv[2])
    fingerprints = None
    dfs = pd.read_csv(path, chunksize=chunksize)
    print("Num processes", num_processes)
    for i, df in enumerate(dfs):
        sample_fingerprints = df.Fingerprint.str.split().values
        # p = Pool(num_processes)
        # try:
        #     blocks = np.split(sample_fingerprints, num_processes)

        #     sample_fingerprints = np.concatenate(
        #         p.map(convert_fingerprint, blocks))
        #     print("Num processes", num_processes)

        # except Exception as e:
        #     print(e)
        sample_fingerprints = convert_fingerprint(sample_fingerprints)
        # p.close()
        # p.join()
        if i+1 % 5 == 0:
            with open(f'./fingerprints/fingerprints{i/5}.pickle', 'wb') as handle:
                pickle.dump(fingerprints, handle,
                            protocol=pickle.HIGHEST_PROTOCOL)
            fingerprints = sample_fingerprints
        else:
            fingerprints = np.concatenate([fingerprints, sample_fingerprints])

    print("DONE")
    # fingerprint_paths = glob.glob('./fingerprints/*')
    # tree = MultibitTree(fingerprints, 'sample_tree')
    # tree.build_tree()


if __name__ == '__main__':
    main()

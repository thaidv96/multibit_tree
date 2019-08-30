from datetime import datetime
import pandas as pd
import numpy as np
import sys
from tree import MultibitTree
import pickle
import numpy as np
import glob


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
    fingerprints = []
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
        if i % 5 == 0:
            print(i)
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


def build_tree():
    finger_files = glob.glob("./fingerprints/*")
    fingerprints = []
    print("Start loading fingerprints", datetime.now())
    for fn in finger_files:
        with open(fn, 'rb') as handle:
            sample_fingerprints = pickle.load(handle)
        fingerprints.append(sample_fingerprints)
    fingerprints = np.concatenate(fingerprints)
    print("Fingerprint loaded", datetime.now())
    tree = MultibitTree(fingerprints, 'sample_tree')
    tree.build_tree()
    print("Tree built completely", datetime.now())


if __name__ == '__main__':
    # main()
    build_tree()

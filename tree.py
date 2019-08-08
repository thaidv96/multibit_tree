import numpy as np


class Node(object):
    def __init__(self,  fingerprint_indices,  idx=None):
        self.idx = idx
        self.fingerprint_indices = fingerprint_indices
        self.must_contains = None
        self.not_contains = None

    def set_idx(self, idx):
        del self.idx
        self.idx = idx

    def set_must_contains(self, must_contains):
        self.must_contains = must_contains

    def set_not_contains(self, not_containts):
        self.not_contains = not_containts

    def set_fingerprint_indices(self, fingerprint_indices):
        del self.fingerprint_indices
        self.fingerprint_indices = fingerprint_indices


class Tree(object):
    def __init__(self):
        self.root = None
        self.i_child = None
        self.o_child = None

    def set_root(self, node):
        self.root = node

    def set_i_child(self, tree):
        self.i_child = tree

    def set_o_child(self, tree):
        self.o_child = tree


class MultibitTree(object):
    def __init__(self, fingerprints):
        self.fingerprints = fingerprints
        self.fingerprint_idx = np.arange(0, fingerprints.shape[1])
        self.tree = None

    def build_tree_recursively(self, root_node):
        fingerprint_indices = root_node.fingerprint_indices

        split_idx = find_split_idx(self.fingerprints[fingerprint_indices])

        idx = split_idx
        root_node.set_idx(idx)

        # Base case (tree dung sinh ra nhanh khi nao???)

        tree = Tree()
        if root_node.idx == None or len(root_node.fingerprint_indices) == 1:
            tree.set_root(root_node)
            return tree

        # Find must contains and not contains set:
        must_contains = self.fingerprint_idx[self.fingerprints[fingerprint_indices].sum(
            axis=0) == len(fingerprint_indices)]
        not_contains = self.fingerprint_idx[self.fingerprints[fingerprint_indices].sum(
            axis=0) == 0]

        root_node.set_must_contains(must_contains)
        root_node.set_not_contains(not_contains)

        # Get requirement for building children
        i_sign = self.fingerprints[fingerprint_indices][:, split_idx] == 1
        i_idx = root_node.fingerprint_indices[i_sign]
        i_root_node = Node(fingerprint_indices=i_idx)

        o_sign = self.fingerprints[fingerprint_indices][:, split_idx] == 0
        o_idx = root_node.fingerprint_indices[o_sign]
        o_root_node = Node(fingerprint_indices=o_idx)
        root_node.set_fingerprint_indices(None)
        tree.set_root(root_node)

        # Get I Child and O Child recursively
        i_child = self.build_tree_recursively(i_root_node)
        o_child = self.build_tree_recursively(o_root_node)
        tree.set_i_child(i_child)
        tree.set_o_child(o_child)
        self.tree = tree
        return tree

    def build_tree(self):
        root_node = Node(np.array(range(len(self.fingerprints))))
        self.build_tree_recursively(root_node)


def find_split_idx(fingerprints):
    # Fingerprints are stored in format:
    # np.array([[1,0,0,1,1,0],[1,0,1,1,0,0]])
    num_fingerprints = fingerprints.shape[0]
    num_occurences_by_cols = fingerprints.sum(axis=0)
    differences = np.abs(num_occurences_by_cols - num_fingerprints/2)
    if differences.min() == num_fingerprints/2:
        return None

    idx = np.argmin(differences)
    return idx


# Test case
fingerprints = np.array([[1, 0, 1, 1, 0, 0],
                         [0, 1, 1, 0, 0, 1],
                         [1, 0, 0, 1, 1, 0],
                         [1, 0, 1, 0, 1, 0],
                         [0, 1, 0, 1, 0, 1],
                         [1, 1, 1, 0, 0, 0]
                         ])

tree = MultibitTree(fingerprints)
tree.build_tree()

mlb = tree.tree

import numpy as np


def get_index_3(x):
    # TODO
    index = np.asarray(x[:, :, 60])/np.asarray(x[:, :, 0])
    return index

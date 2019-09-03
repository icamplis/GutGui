import numpy as np


# Example index 3
def get_index_3(x):
    index = np.gradient(x[:, :, 0] + x[:, :, 10] + x[:, :, 20] + x[:, :, 30])
    return index

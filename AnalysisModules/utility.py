import numpy as np

def read(file_to_read):
    data = np.fromfile(file_to_read, dtype='>f')  # returns 1D array and reads file in big-endian binary format
    data_cube = data[3:].reshape(640, 480, 100)  # reshape to data cube and ignore first 3 values which are wrong
    return data_cube


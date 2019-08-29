def get_index_8(x):
    index = (x[:, :, 60] + x[:, :, 61])/2
    print('in correct index (8)')
    print(x[0, :10, 60])
    print(x[0, :10, 61])
    print(index[0, :10])
    print('out of index')
    return index
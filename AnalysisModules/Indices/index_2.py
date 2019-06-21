def get_index_2(x_absorbance):
    index = (x_absorbance[:,:,61] +
             x_absorbance[:,:,62] +
             x_absorbance[:,:,63] +
             x_absorbance[:,:,64] +
             x_absorbance[:,:,65] +
             x_absorbance[:,:,66])/6
    return index
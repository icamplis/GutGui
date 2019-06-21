def get_index_1(x_absorbance):
    index = (x_absorbance[:,:,60] +
             x_absorbance[:,:,61] +
             x_absorbance[:,:,62] +
             x_absorbance[:,:,63] +
             x_absorbance[:,:,64] +
             x_absorbance[:,:,65] +
             x_absorbance[:,:,66])/7
    return index
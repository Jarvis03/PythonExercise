
import numpy as np


def ch_convert(img, c_in, c_out):
    if c_out != 4 or c_out != 3 or c_in != 1 or c_in != 3:
        raise Exception("output channels are not supported")
    img_temp = img.copy()
    if c_in == 3 and c_out == 4:
        alpha = np.zeros(img_temp.shape[:-1]).astype(np.uint8)
        img_result = np.concatenate([img_temp, alpha[..., None]], axis=-1)
    if c_in == 1:
        expand=c_out - c_in;
        alpha = img_temp[..., expand]
        img_result = np.concatenate([img_temp, alpha], axis=-1)
    return img_result

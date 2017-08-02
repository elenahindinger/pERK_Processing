from __future__ import division
import numpy as np
from skimage import io
from natsort import natsorted
import os

__author__ = 'Elena Maria Daniela Hindinger'

''' This code normalises sum stacks in a folder. Run this after the ImageJ macro pERK_aligned_post_processing.ijm and
afterwards, average groups in image J and draw a mask, then run the pERK quantification code in python.'''


input_folder = r'J:\Elena Hindinger\PERK\lm2\analysis batch 2\aligned sum stacks'
input_list = natsorted(os.listdir(input_folder))
basepath, folder = os.path.split(input_folder)
output_folder = os.path.join(basepath, 'normalised sum stacks')
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


def normalise (fish):
    return (fish / np.max(fish) * 255).astype('uint8')


for file in input_list:
    if file[-4:] == '.tif':
        print 'Processing file ', file
        img_path = os.path.join(input_folder, file)
        img = io.imread(img_path, plugin='tifffile')
        normalised_img = normalise(img)
        savename = os.path.join(output_folder, file.replace('.tif', '_normalised.tif'))
        io.imsave(savename, normalised_img)
    else:
        pass
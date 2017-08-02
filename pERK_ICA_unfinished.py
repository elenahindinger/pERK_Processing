from __future__ import division
import numpy as np
from skimage import io
from natsort import natsorted
import os
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import nrrd
from sklearn.decomposition import FastICA

__author__ = 'Elena Maria Daniela Hindinger'

input_folder = r'J:\Elena Hindinger\PERK\lm2\pERK ICA\aligned pERK stacks'
input_list = natsorted(os.listdir(input_folder))
output_folder = r'J:\Elena Hindinger\PERK\lm2\pERK ICA\normalised aligned pERK stacks'


def normalise (fish):
    return (fish / np.max(fish) * 255).astype('uint8')

for subfolder in input_list[1:]:
    subfolder_path = os.path.join(input_folder, subfolder)
    subfolder_list = natsorted(os.listdir(subfolder_path))
    if not os.path.exists(os.path.join(output_folder, subfolder)):
        os.makedirs(os.path.join(output_folder, subfolder))
    for file in subfolder_list:
        img_path = os.path.join(subfolder_path, file)
        if file.endswith('.tif'):
            print 'Processing file ', file
            # img32, options = nrrd.read(img_path)
            # reordered_array = np.swapaxes(img32, axis1=0, axis2=2)
            reordered_array = io.imread(img_path, plugin='tifffile')
            normalised_img = normalise(reordered_array)
            savename = os.path.join(output_folder, subfolder, file.replace('.tif', '_normalised.tiff'))
            io.imsave(savename, normalised_img)
        else:
            pass

for subfolder in natsorted(os.listdir(output_folder)):
    subfolder_path = os.path.join(output_folder, subfolder)
    subfolder_list = natsorted(os.listdir(subfolder_path))
    stack_list = []
    for file in subfolder_list:
        print 'Processing file ', file
        img_path = os.path.join(subfolder_path, file)
        stack = io.imread(img_path, plugin='tifffile')
        stack_list.append(stack.flatten())
    all_stacks = np.stack(stack_list, axis=0)
    normalised_all = normalise(all_stacks)

ica = FastICA(n_components=5)
X = ica.fit_transform(normalised_all)
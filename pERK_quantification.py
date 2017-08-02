from __future__ import division
import numpy as np
from skimage import io
from natsort import natsorted
import os
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

__author__ = 'Elena Maria Daniela Hindinger'

input_folder = r'J:\Elena Hindinger\PERK\lm2\analysis batch 2\masked pixel data'
input_list = natsorted(os.listdir(input_folder))
output_folder = r'J:\Elena Hindinger\PERK\lm2\analysis batch 2'
conditions = ['gr DMSO', 'gr Fluoxetine', 'het DMSO', 'het Fluoxetine']
# all_data = []
all_data = pd.DataFrame()
counter = 0
for file in input_list:
    filepath = os.path.join(input_folder, file)
    df = pd.read_csv(filepath)
    df = df.drop(df.columns[0], axis=1)
    array = df.values.flatten()
    df = pd.DataFrame(array)
    df['Treatment Condition'] = conditions[counter]
    all_data = pd.concat([all_data, df], axis=0)
    counter += 1
    # all_data.append(array)

all_data.columns = ['Pixel Intensity', 'Treatment Condition']


def distribution_plots(data, plottype, outdir):
    colors = ["b", "r", "g", "purple"]
    sns.set_style('white')
    fig, ax = plt.subplots()
    sns.set(style="ticks")
    if plottype == 'box':
        ax = sns.boxplot(x="Treatment Condition", y="Pixel Intensity", data=data, palette=colors)
    elif plottype == 'violin':
        ax = sns.violinplot(x="Treatment Condition", y="Pixel Intensity", data=data)
    elif plottype == 'lv':
        ax = sns.lvplot(x="Treatment Condition", y="Pixel Intensity", data=data)
    else:
        assert False
    sns.despine(offset=10, trim=True)
    ax.set_xlabel('Treatment Condition', fontsize=18)
    ax.set_ylabel('Range of Pixel Values', fontsize=18)
    ax.tick_params(labelsize=14)
    plt.suptitle('Distribution of Pixel Intensity Values per Treatment Condition', fontsize=18)
    savename = os.path.join(outdir, plottype + '_plot.tiff')
    fig.savefig(savename, format='tiff', bbox_inches='tight', dpi=300)
    savename1 = os.path.join(outdir, plottype + '_plot.pdf')
    fig.savefig(savename1, format='pdf', bbox_inches='tight', dpi=300)
    savename2 = os.path.join(outdir, plottype + '_plot.svg')
    fig.savefig(savename2, format='svg', bbox_inches='tight', dpi=300)
    plt.close('all')


def cumulative_distribution(data, outdir):
    all_data = data.copy()
    gb = all_data.groupby('Treatment Condition')
    gb.groups
    gr = gb.get_group('gr DMSO')
    het = gb.get_group('het DMSO')
    gr_fluox = gb.get_group('gr Fluoxetine')
    # het_fluox = gb.get_group('het Fluoxetine')
    sns.set_style('white')
    fig, ax = plt.subplots()
    plt.margins(0.1)
    ax = sns.kdeplot(gr['Pixel Intensity'], cumulative=True, cut=0, ax=ax, label='gr DMSO')
    ax = sns.kdeplot(het['Pixel Intensity'], cumulative=True, cut=0, ax=ax, label='het DMSO')
    ax = sns.kdeplot(gr_fluox['Pixel Intensity'], cumulative=True, cut=0, ax=ax, label='gr Fluoxetine')
    # ax = sns.kdeplot(het_fluox['Pixel Intensity'], cumulative=True, clip=(0, 255), ax=ax, label='het Fluoxetine')
    ax.set_xlabel('Pixel Intensity', fontsize=18)
    ax.set_ylabel('Cumulative Proportion of Pixels', fontsize=18)
    plt.suptitle('Treatment-specific CDF of Pixel Values', fontsize=18)
    ax.tick_params(labelsize=14)
    savename = os.path.join(outdir, 'cumulative_distribution.tiff')
    fig.savefig(savename, format='tiff', bbox_inches='tight', dpi=300)
    savename1 = os.path.join(outdir, 'cumulative_distribution.pdf')
    fig.savefig(savename1, format='pdf', bbox_inches='tight', dpi=300)
    savename2 = os.path.join(outdir, 'cumulative_distribution.svg')
    fig.savefig(savename2, format='svg', bbox_inches='tight', dpi=300)
    plt.close('all')

cumulative_distribution(all_data, output_folder)
distribution_plots(all_data, plottype='box', outdir=output_folder)
# distribution_plots(all_data, plottype='violin', outdir=output_folder)
# distribution_plots(all_data, plottype='lv', outdir=output_folder)

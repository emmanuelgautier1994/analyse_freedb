import re
from itertools import product

import codecs
import csv
from os import listdir
from os.path import isfile, join
import glob

import time
import random

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import engine

_ROOT_ = "" #The path where freedb is stored
_GENRES_ = ["blues", "classical", "country", "data", "folk", "jazz", "misc", "newage", "reggae", "rock", "soundtrack"]
                    

# The following dictionary contains the IDs of albums by Taylor Swift, obtained using engine.getAllIDsOfArtist(_ROOT_, "Taylor Swift", _GENRES_)
dict_TS = {}
dict_TS["misc"] = ['0312b113', '0f055502', '1206f602', '1e101e13', '1f0ecb12', '27101d13', '2f053b04', '36049006', '3f05f106', 'ae0c9f0d', 'af0d110f', 'b00c9c0d', 'b00d110f', 'bd0fcf0e', 'bf0e260f', 'c90cca0d', 'cd0f0710', 'd30c2a0e', 'd30fb60e', 'd8120210', 'dd0f8910', 'fa0f4c10', 'fc0f6c10', 'fe12b113']
dict_TS["rock"] = ['0200db01', '02104113', '1112dd13', '2a124813', '36049006', '3d049b05', '8c09930b', 'cf0d4b0f', 'db0d2f0f', 'f0100711', 'fa0f4c10']
dict_TS["data"] = ['1001ac02', '6c11df09', '85097d0b', 'bd0fcf0e', 'be0eed0e', 'ca103410']
dict_TS["folk"] = ['fa0f4c10']
dict_TS["blues"] = ['0200c001', '27101d13', 'ca103410']
dict_TS["country"] = ['010f5010', '16103b12', '1c025e03', '1e122114', '2c125714', '2d123214', '31125614', '36049006', '3d048006', '3f05f106', '41048506', '41048706', '42049a06', '4805d806', '4905d906', '4c049006', '4f049a06', '50049106', '52049506', '52049a06', '540ba607', '56128a07', '61068608', '64080b08', '66081008', '6c11df09', '6f09720b', '7c097d0b', '800c110c', '85097d0b', '85097f0b', '8509930b', '8809910b', '8c09910b', '8e09920b', '8f0c100c', '910a690c', '9309a60b', '970c1b0c', '970c1d0c', 'a90b6f0d', 'ac0b700d', 'af0c9a0d', 'b00c9a0d', 'b30fd80d', 'b50ca40d', 'b50caa0f', 'b50cc00f', 'b60d130f', 'b612af10', 'b70c980f', 'b70d130f', 'b70d140f', 'bb0cb20d', 'bb0fd00e', 'bd0fcf0e', 'be0c880f', 'be0ca60d', 'be0eeb0e', 'be0fcf0e', 'bf0c870d', 'bf0c990d', 'bf0eed0e', 'c00cb30d', 'c00fe90e', 'c10cb20d', 'c10d310f', 'c20fc70e', 'c40cb20d', 'c40cc70f', 'c70fd10e', 'c80c9b0d', 'c8128d10', 'ca103410', 'ca103610', 'cb103410', 'ce0fb50e', 'd20e060f', 'd8120210', 'f1129310', 'f512af13', 'f8101911', 'f90f6b10', 'fa0f4c10', 'fa126514', 'fc0f4d10', 'fe12b113']

# Setting up seaborn for visualization
nb_x = 3
nb_y = 4

pal = sns.color_palette("nipy_spectral", 12)
sns.set_style("darkgrid")

fig, axes= plt.subplots(nb_x, nb_y)
count = 0

# Reading Taylor Swift's data from the csv created using engine.sumArtist(_ROOT_, "Taylor Swift", _GENRES_)
print("TS")
DF_TS = pd.read_csv(_ROOT_ + "sums_by_artist/summary_taylor_swift.csv", sep=';')
c_TS = DF_TS.loc[:,"stdev pc"]
c_TS = c_TS[c_TS <= 1]

# Reading genres' data from the csv's created using engine.sumGenre(_ROOT_, g), looping for g in _GENRES_
# Also, plotting the data
for g in _GENRES_:
    print(g)
    DF_g = pd.read_csv(_ROOT_ + "sums_by_genre/summary_" + g + ".csv", sep=';')
    c = DF_g.loc[:,"stdev pc"]
    c = c[c <= 1]
    f = sns.distplot(c, axlabel = g, kde = False, color = pal[count], ax=axes[int(count / nb_y), count % nb_y])
    f.set(yticks = [])
    f = sns.distplot(c_TS, axlabel = g, kde = False, hist = False, rug = True, color = "k", ax=axes[int(count / nb_y), count % nb_y])
    f.set(yticks = [])
    count+=1

# Plotting Taylor Swift's data
f = sns.distplot(c_TS, axlabel = "Taylor Swift", kde = False, color = pal[count], ax=axes[int(count / nb_y), count % nb_y])
f.set(yticks = [])

# Finishing touches
sns.despine(left=True)

plt.subplots_adjust(hspace = 0.5)

plt.show()

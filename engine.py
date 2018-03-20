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

_ROOT_ = "" #The path where freedb is stored
_GENRES_ = ["blues", "classical", "country", "data", "folk", "jazz", "misc", "newage", "reggae", "rock", "soundtrack"]

def truncate(f, n):
    #Truncates/pads a float f to n decimal places without rounding
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def getID(filename, verbose=None):
        if verbose == None:
                verbose = False
        
        #Opening file
        file = codecs.open(filename, "r", encoding='utf-8')
        
        if verbose:
                print("File opened")

        try:
                 text = file.read()
        except UnicodeDecodeError:
                if verbose:
                        print("Unicode Decoding Error")
                        return 0

        D_ID = re.search("(?<=DISCID=)\w+", text).group(0)

        return D_ID

def getArtist(filename, verbose=None):
        if verbose == None:
                verbose = False
        
        #Opening file
        file = codecs.open(filename, "r", encoding='utf-8')
        
        if verbose:
                print("File opened")

        try:
                 text = file.read()
                 artist_search = re.search("(?<=DTITLE=).*(?= /)", text)
                 if artist_search == None:
                         return ""
                 else:
                         return artist_search.group(0)
        except UnicodeDecodeError:
                if verbose:
                        print("Unicode Decoding Error")
                        return 0
        

def getAllData(filename, verbose=None):
        if verbose == None:
                verbose = False
        
        #Opening file
        file = codecs.open(filename, "r", encoding='utf-8')
        
        if verbose:
                print("File opened")

        text = file.read()
        
        #Reading offsets from file
        offsets = []

        OS_text = re.search(".+seconds", text, re.DOTALL).group(0)

        for o in re.findall("[0-9]+", OS_text):
                offsets += [int(o)]

        offsets[len(offsets)-1] *= 75
        disc_length = offsets[len(offsets)-1]

        if verbose:
                print("Offsets read:")
                print(offsets)
        
        #Computing track lengths (in frames) from offset deltas
        lengths = []

        for i in range(1,len(offsets)):
                lengths += [offsets[i] - offsets[i-1]]

        if verbose:
                print("Track lengths computed:")
                print(lengths)
        
        #Computing statistics

        if lengths != []:
                std = np.std(lengths)
                avg = disc_length/len(lengths)
                amp = max(lengths) - min(lengths)
        else:
                std = 0
                avg = 0
                amp = 0

        if avg != 0:
                rel_std = std/avg
                rel_amp = amp/avg
        else:
                rel_std = 0
                rel_amp = 0

        std = int(std)
        avg = int(avg)

        rel_std = truncate(rel_std, 4)
        rel_amp = truncate(rel_amp, 4)

        if verbose:
                print("Stats computed:")
                print("average length: " + str(avg))
                print("strandard deviation: " + str(std) + " (" + str(100*rel_std) + " % of avg)")
                print("amplitude: " + str(amp) + " (" + str(100*rel_amp) + " % of avg)")

        #Reading additional metadata
        D_ID = ''
        D_artist = ''
        D_genre = ''
        
        try:
                D_ID = re.search("(?<=DISCID=)\w+", text).group(0)
        except AttributeError:
                pass

        try:
                D_artist = re.search("(?<=DTITLE=).*(?= /)", text).group(0)
        except AttributeError:
                pass

        try:
                D_genre = re.search("(?<=DGENRE=)\w+", text).group(0)
        except AttributeError:
                pass

        if verbose:
                print("Metadata computed")

        dict_res = {'genre' : D_genre, 'id' : D_ID, 'length' : disc_length, 'avg l' : avg, 'stdev' : std, 'stdev pc' : rel_std, 'amp' : amp, 'amp pc' : rel_amp}
        return dict_res

def isByArtist(filename, artist):
        #Opening file
        file = codecs.open(filename, "r", encoding='utf-8')

        #Reading artist
        try:
                text = file.read()
                D_title = re.search("(?<=DTITLE=).*", text).group(0)

                if re.search(artist + ".*/",D_title) != None:
                        return True
                
        except UnicodeDecodeError:
                pass
        
        return False

def getIDsOfArtist(root, genre, artist):
        IDs = []

        print("Scanning " + genre + " for albums by " + artist)

        count = 0

        for filename in glob.iglob(root + genre + "/" + "*"):
                count += 1
                if count % 25000 == 0:
                        print("Now " + str(count) + " albums scanned")
                if getArtist(filename) == artist:
                        ID = getID(filename)
                        IDs += [ID]
                        print(ID)

        print("Found " + str(len(IDs)) + " IDs for " + genre + " albums by " + artist)
        print(IDs)
        return IDs

def getAllIDsOfArtist(root, artist, genresToScan = None):
        if genresToScan == None:
                genresToScan = _GENRES_
        
        dict_artist = {}
        
        for g in genresToScan:
                dict_artist[g]= getIDsOfArtist(root, g, artist)

        return dict_artist

def sumGenre(root, genre, verbose=None):
        if verbose ==  None:
                verbose = False
        
        with open (root + 'summary_' + genre + '.csv', 'w+') as csvfile:
                fieldnames = ['genre', 'id', 'length', 'avg l', 'stdev', 'stdev pc', 'amp', 'amp pc']
                albumwriter = csv.DictWriter(csvfile, fieldnames, delimiter=';')

                albumwriter.writeheader()
                
                print("Scanning " + genre)

                count_s = 0

                count_y = 0
                count_a_err = 0
                count_ud_err = 0
                count_ue_err = 0

                start = time.time()

                minutes_elapsed = 0

                for filename in glob.iglob(root + genre + "/" + "*"):
                        count_s += 1
                        if count_s % 25000 == 0:
                                print("Now " + str(count_s) + " albums scanned")

                        if time.time() - start > (minutes_elapsed + 1)*60:
                                minutes_elapsed += 1
                                if minutes_elapsed % 10 == 0:
                                        print(str(minutes_elapsed) + " minutes elapsed")
                        try:
                                dict_CD = getAllData(filename)
                                albumwriter.writerow(dict_CD)
                                count_y += 1
                        except AttributeError:
                                count_a_err +=1
                                if verbose:
                                        print("Failed to parse on " + filename)
                        except UnicodeDecodeError:
                                count_ud_err += 1
                                if verbose:
                                        print("Failed to decode " + filename)
                        except UnicodeEncodeError:
                                count_ue_err += 1
                                if verbose:
                                        print("Failed to encode" + filename)

                finish = time.time()

                print("Done with " + genre + " in " + str(int((finish - start)/60)) + " min " + str(int(finish - start) % 60) + " sec!")
                print("Wrote " + str(count_y) + " lines")
                print("Encountered " + str(count_a_err) + " parsing errors")
                print("Encountered " + str(count_ud_err) + " decoding errors")
                print("Encountered " + str(count_ue_err) + " encoding errors")

def sumArtist(root, artist, genresToScan = None, verbose=None):
        if verbose ==  None:
                verbose = False

        if genresToScan == None:
                genresToScan = _GENRES_
        
        keepcharacters = (' ','.','_')
        artist_for_path = "".join(c for c in artist if c.isalnum() or c in keepcharacters).rstrip().lower().replace(" ", "_")
        
        
        with open (root + 'summary_' + artist_for_path + '.csv', 'w+') as csvfile:
                fieldnames = ['genre', 'id', 'length', 'avg l', 'stdev', 'stdev pc', 'amp', 'amp pc']
                albumwriter = csv.DictWriter(csvfile, fieldnames, delimiter=';')

                albumwriter.writeheader()

                artist_dict = getAllIDsOfArtist(root, artist, genresToScan)

                for g in artist_dict.keys():
                        print("Writing " + g + " songs by " + artist)

                        for ID in artist_dict[g]:
                                filename = root + g + "/" + ID
                                try:
                                        dict_CD = getAllData(filename)
                                        albumwriter.writerow(dict_CD)
                                except AttributeError:
                                        if verbose:
                                                print("Failed to parse on " + filename)
                                except UnicodeDecodeError:
                                        if verbose:
                                                print("Failed to decode " + filename)
                                except UnicodeEncodeError:
                                        if verbose:
                                                print("Failed to encode" + filename)

                        print("Done!")
                    

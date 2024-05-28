import numpy as np
import pandas as pd
import sys, os, time
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances

st = time.time()

# argument is the path to analyze
# default is the current path
try:
    top=Path(sys.argv[1])
except:
    top=Path(os.getcwd())
print('top-level folder:', top)

# dataframe for list of files
# for this version only .txt files are processed
df = pd.DataFrame(columns=['path', 'name', 'type', 'text'])

# to count numbers of files, and list of files that couldn't be read
total_no_files, no_files, no_skipped, files_skipped = 0, 0, 0, list()

# filter on .txt files and write to dataframe
for path in top.rglob('*'):
    spath = str(path)
    if spath[-4:]=='.txt':
        nam =  spath[spath.rfind('/')+1:]
        typ =  spath[spath.rfind('.')+1:]
        with open(spath) as f:
            try:
                txt = f.read()
                no_files+=1
            except:
                no_skipped+=1
                files_skipped.append(spath)
        df.loc[len(df)] = [path, nam, typ, txt]

# show stats
print('total number of files in folder:', total_no_files)
print('no. of files in comparison:', no_files)
print('no. of files skipped:', no_skipped)
print('files skipped:')

# list files that couldn't be read
for f in files_skipped:
    print(f)

# initialize tf-idf vectorizer
vectorizer = TfidfVectorizer(lowercase=False)

# train/fit: create vectors from text
vectors = vectorizer.fit_transform(df.text)

# calculate similarities between all files
# creates a symmetrical matrix around the diagonal (row=col) axis
similarities=cosine_similarity(vectors)

# calculate differences between all files
# another symmetrical matrx
differences=euclidean_distances(vectors)

# dictionaries to record similarities and differences
sim_dict, diff_dict = dict(), dict()

# iterate over all cells in the matrix
# skipping the row<=col half
# write to dictionary
for i in range(similarities.shape[0]):
    for j in range(i+1):
        if i==j:
            continue
        sim_dict[(i,j)] = similarities[i][j]

# reverse sort dictionary
sim_dict = dict(sorted(sim_dict.items(), key=lambda item: item[1], reverse=True))

# create diffs dict
for i in range(differences.shape[0]):
    for j in range(i+1):
        if i==j:
            continue
        diff_dict[(i,j)] = differences[i][j]

# dataframe for results
df_results = pd.DataFrame(columns=['path1', 'path2', 'similarity', 'difference'])

# populate dataframe from dictionaries
for (k, v) in sim_dict.items():
    df_results.loc[len(df_results)] = [df.iloc[k[0]]['path'], df.iloc[k[1]]['path'], v, diff_dict[k]]

# output to csv
df_results.to_csv('comparison.csv')
print('file comparisons saved to comparison.csv')

# write elapsed time
et = time.time()
print('elapsed time:', et - st, 'seconds.')




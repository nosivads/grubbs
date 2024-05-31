import numpy as np
import pandas as pd
import sys, os, time
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances

st = time.time()

# arguments are the paths to compare
# default is the current path
try:
    top1=Path(sys.argv[1])
except:
    top1=Path(os.getcwd())
try:
    top2=Path(sys.argv[2])
except:
    top2=Path(os.getcwd())
print('folders to compare:', top1, top2)

# dataframe for list of files
# for this version only .txt files are processed
df1 = pd.DataFrame(columns=['path', 'name', 'type', 'text'])
df2 = pd.DataFrame(columns=['path', 'name', 'type', 'text'])

filetypes = ['.txt', '.docx']

def read_files(top, filetypes, df):
    
    for path in top.rglob('*'):

        if path.name[0]!='.':

            if path.suffix in filetypes:

                with open(str(path)) as f:
                
                    try:
                        df.loc[len(df)] = [str(path), path.name, path.suffix, f.read()]
                    except:
                        pass
    
    return df

read_files(top1, 'txt', df1)
read_files(top2, 'txt', df2)

# initialize tf-idf vectorizer
vectorizer = TfidfVectorizer(lowercase=False)

# train/fit: create vectors from text
vectors1 = vectorizer.fit_transform(df1.text)
vectors2 = vectorizer.fit_transform(df2.text)

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




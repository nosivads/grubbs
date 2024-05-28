import numpy as np
import pandas as pd
import sys, os, time
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances

st = time.time()

try:
    top=Path(sys.argv[1])
except:
    top=Path(os.getcwd())
print('top-level folder:', top)

df = pd.DataFrame(columns=['path', 'name', 'type', 'text'])

total_no_files, no_files, no_skipped, files_skipped = 0, 0, 0, list()

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

print('total number of files in folder:', total_no_files)
print('no. of files in comparison:', no_files)
print('no. of files skipped:', no_skipped)
print('files skipped:')
for f in files_skipped:
    print(f)

vectorizer = TfidfVectorizer(lowercase=False)
vectors = vectorizer.fit_transform(df.text)

similarities=cosine_similarity(vectors)
differences=euclidean_distances(vectors)

sim_dict, diff_dict = dict(), dict()

for i in range(similarities.shape[0]):
    for j in range(i+1):
        if i==j:
            continue
        sim_dict[(i,j)] = similarities[i][j]
sim_dict = dict(sorted(sim_dict.items(), key=lambda item: item[1], reverse=True))

for i in range(differences.shape[0]):
    for j in range(i+1):
        if i==j:
            continue
        diff_dict[(i,j)] = differences[i][j]

df_results = pd.DataFrame(columns=['path1', 'path2', 'similarity', 'difference'])

for (k, v) in sim_dict.items():
    df_results.loc[len(df_results)] = [df.iloc[k[0]]['path'], df.iloc[k[1]]['path'], v, diff_dict[k]]

df_results.to_csv('comparison.csv')
print('file comparisons saved to comparison.csv')

et = time.time()
print('elapsed time:', et - st, 'seconds.')




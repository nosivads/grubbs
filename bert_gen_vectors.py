from sentence_transformers import SentenceTransformer
from transformers import pipeline

import pandas as pd
import numpy as np
'''
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
'''
import sys, os
from pathlib import Path

from spire.doc import *
from spire.doc.common import *
'''
import datetime, json
'''
try:
    top=Path(sys.argv[1])
except:
    top=Path(os.getcwd())
try:
    out=Path(sys.argv[2])
except:
    out=Path('embeddings.csv')

bert_model = SentenceTransformer('bert-base-nli-mean-tokens')

embeddings_df = pd.DataFrame(columns=['folder', 
                           'filename',
                           'text',
                           'length'])

i = 0
for path in top.rglob('*'):

    if path.suffix == '.txt':
        text = path.read_text()
    elif path.suffix == '.doc' or path.suffix == '.docx':
        spath = str(path)
        document = Document()
        document.LoadFromFile(spath)
        text = document.GetText().replace('Evaluation Warning: The document was created with Spire.Doc for Python.', '')
    else:
        continue

    print('processing...', path.parent, path.name)
    i += 1
    embeddings_df.loc[len(embeddings_df)] = [path.parent,
                                             path.name,
                                             text,
                                             len(text)]

print('creating embeddings...')
embeddings_df['embedding'] = embeddings_df.text.apply(lambda x: bert_model.encode(x))
    
print('writing CSV...')
embeddings_df.to_csv(out)

print('number of files:', i)
print('output:', out)
        
                           


from sentence_transformers import SentenceTransformer
from transformers import pipeline

import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances

import sys, os
from pathlib import Path

from spire.doc import *
from spire.doc.common import *

import eml_parser, datetime, json

try:
    top=Path(sys.argv[1])
except:
    top=Path(os.getcwd())
try:
    out=Path(sys.argv[2])
except:
    out='embeddings.csv'

# for email parsing
def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

bert_model = SentenceTransformer('bert-base-nli-mean-tokens')

df = pd.DataFrame(columns=['folder', 
                           'filename',
                           'length',
                           'embedding'])

i = 0
for path in top.rglob('*'):
    if path.suffix == '.txt':
        text = path.read_text()
    elif path.suffix == '.doc' or path.suffix == '.docx':
        spath = str(path)
        document = Document()
        document.LoadFromFile(spath)
        text = document.GetText().replace('Evaluation Warning: The document was created with Spire.Doc for Python.', '')
    elif path.suffix == '.eml':
        with open(path, 'rb') as f:
            raw_email = f.read()
            print(raw_email)
        ep = eml_parser.EmlParser()
        parsed_eml = ep.decode_email_bytes(raw_email)
        text = json.dumps(parsed_eml, default=json_serial)
    else:
        continue
    embedding = bert_model.encode(text)
    print('processing...', path.parent, path.name)
    i += 1
    df.loc[len(df)] = [path.parent,
                       path.name,
                       len(text),
                       embedding]
    
df.to_csv(out)

print('number of files:', i)
print('output written to:', out)
        
                           


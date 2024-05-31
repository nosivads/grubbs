from sentence_transformers import SentenceTransformer

import pandas as pd
import sys, os
from pathlib import Path

from docx import Document

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

i = 1

for path in top.rglob('*'):

    if path.name[0] != '.':
        
        if path.suffix == '.txt':

            text = path.read_text()
            i += 1

        elif path.suffix == '.docx':

            try:

                doc = Document(str(path))
                text_list = []
                for paragraph in doc.paragraphs:
                    text_list.append(paragraph.text)
                    '\n'.join(text_list)
                text = '\n'.join(text_list)
                i += 1

            except:

                continue

        else:

            continue

        print('processing...', path.parent, path.name)
        embeddings_df.loc[len(embeddings_df)] = [path.parent,
                                                 path.name,
                                                 text,
                                                 len(text)]
        
        if i>100:
            break

print('creating embeddings...')
embeddings_df['embedding'] = embeddings_df.text.apply(lambda x: bert_model.encode(x))
    
print('writing pickle file...')
embeddings_df.to_pickle(out)

print('number of files:', i)
print('output:', out)
        
                           


# default model: https://huggingface.co/dbmdz/bert-large-cased-finetuned-conll03-english

from transformers import pipeline
from pathlib import Path

import pandas as pd
import sys, os
'''
from spire.doc import *
from spire.doc.common import *
'''
from docx import Document

try:
    top=Path(sys.argv[1])
except:
    top=Path(os.getcwd())

ner = pipeline(task="ner", aggregation_strategy = 'simple')

df = pd.DataFrame(columns=['folder', 
                           'filename',
                           'entity', 
                           'score', 
                           'word', 
                           'start', 
                           'end'])

i=1

for path in top.rglob('*'):

    if path.name[0] != '.':

        if path.suffix == '.txt':

            text = path.read_text()

        elif path.suffix=='.docx':

            doc = Document(str(path))
            text_list = []
            for paragraph in doc.paragraphs:
                text_list.append(paragraph.text)
                '\n'.join(text_list)
            text = '\n'.join(text_list)
        
        else:

            continue
            
        print('processing #'+str(i), str(path))
        entities = ner(text)

        for entity in entities:

            df.loc[len(df)] = [path.parent,
                               path.name,
                               entity['entity_group'],
                               entity['score'],
                               entity['word'],
                               entity['start'],
                               entity['end']]

        i+=1
        if i>50:
            break

df.to_csv('entities.csv')

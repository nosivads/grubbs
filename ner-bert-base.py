from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

from pathlib import Path

import pandas as pd
import sys, os

from docx import Document

try:
    top=Path(sys.argv[1])
except:
    top=Path(os.getcwd())

tokenizer = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")

ner = pipeline("ner", model=model, tokenizer=tokenizer)

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
                               entity['entity'],
                               entity['score'],
                               entity['word'],
                               entity['start'],
                               entity['end']]

        i+=1
        if i>50:
            break

df.to_csv('entities-bert-base.csv')

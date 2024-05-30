from transformers import pipeline
import pandas as pd
import sys, os
from pathlib import Path

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

for path in top.rglob('*'):
    if path.suffix == '.txt':
        entities = ner(path.read_text())
        print(str(path))
        for entity in entities:
            df.loc[len(df)] = [path.parent,
                               path.name,
                               entity['entity_group'],
                               entity['score'],
                               entity['word'],
                               entity['start'],
                               entity['end']]

df.to_csv('entities.csv')

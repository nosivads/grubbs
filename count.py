#from transformers import pipeline
#import pandas as pd
import sys, os
from pathlib import Path

try:
    top=Path(sys.argv[1])
except:
    top=Path(os.getcwd())

no_files = 0
total_len = 0
max_len = 0
min_len = 10000

for path in top.rglob('*'):
    if path.suffix == '.txt':
        file_len = len(path.read_text())
        total_len += file_len
        no_files += 1
        if file_len > max_len:
            max_len = file_len
        if file_len > 1000 and file_len < min_len:
            min_len = file_len
        print(no_files)

print('=====')
print('average length:', total_len/no_files)
print('minimum length:', min_len)
print('maximum length:', max_len)




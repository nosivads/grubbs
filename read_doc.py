from spire.doc import *
from spire.doc.common import *
from pathlib import Path
import pandas as pd

df = pd.DataFrame(columns=['path', 'text'])

top=Path(sys.argv[1])

i = 0

for path in top.rglob('*'):
    spath = str(path)
    if spath[spath.rfind('/')+1]!='.' and (spath[-4:]=='.doc' or spath[-5]=='.docx'):
        print(spath)
        document = Document()
        document.LoadFromFile(spath)
        document_text = document.GetText()
        document_text = document_text.replace('Evaluation Warning: The document was created with Spire.Doc for Python.', '')
        print(document_text)
        document.Close()
        i += 1
        df.loc[len(df)] = [spath, document_text]

print('\n\n', i, 'files')

df.to_csv('texts.csv')




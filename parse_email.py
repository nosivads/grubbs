import datetime
import json
import eml_parser

# argument is the path to analyze
# default is the current path
try:
    top=Path(sys.argv[1])
except:
    top=Path(os.getcwd())
print('top-level folder:', top)



def json_serial(obj):
  if isinstance(obj, datetime.datetime):
      serial = obj.isoformat()
      return serial

with open('sample.eml', 'rb') as fhdl:
  raw_email = fhdl.read()

ep = eml_parser.EmlParser()
parsed_eml = ep.decode_email_bytes(raw_email)

print(json.dumps(parsed_eml, default=json_serial))
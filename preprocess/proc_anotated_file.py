#!/usr/bin/env python
import sys
import json
import preprocess as pre


f_in = sys.argv[1]
f_out = f_in.replace('.xlsx', '_pre.json')

if '.xlsx' in f_in:
    ano_file = AnotatedConverter(f_in)
    f_in = ano_file.write_to_json()

json_data = []
with open(f_in, 'r') as f:
    json_data = json.load(f)
    if None != json_data['data']:
        json_data = json.loads(json.dumps(json_data['data']))

tmp_json = json_data
tmp_json = pre.clean_up(tmp_json)

for d in tmp_json:
    d = pre.preprocess_lower(d)
    d = pre.preprocess_sw_rem(d) 
    d = pre.preprocess_stem(d)
    d = pre.preprocess_swrem_stem(d)
    
    # Delete not related
    del d['content']
    

with open(f_out, 'w') as f:
    json.dump(tmp_json, f, indent=4)

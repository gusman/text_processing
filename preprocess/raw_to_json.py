import json
import re
import sys
import os
import csv


def get_source_from_fname(fname):
    lst = fname.split('.')
    return lst[0]

def load_json(f_path):
    news = None
    with open(f_path, 'r') as f:
        news = json.load(f)
    return news

def construct_json_file(f_path, tmp_path, n_last_char):
    with open(f_path, 'rb') as f:
        with open(tmp_path, 'wb+') as f_tmp:
            f_tmp.write(b'[\r\n')
            f.seek(0, 0)
            f_tmp.write(f.read())
            
            # -- Fix end file -- #
            f_tmp.seek(-n_last_char, os.SEEK_END)
            last_str = f_tmp.read(n_last_char)
            last_str = last_str.replace(b',', b'')
            last_str = last_str.replace(b'\r', b'')
            last_str = last_str.replace(b'\n', b'')
            last_str += b'\r\n]'
            f_tmp.seek(-n_last_char, os.SEEK_END)
            f_tmp.write(last_str)

def write_json_file(json_file, data):
    with open(json_file, 'w', newline='') as j_file:
         json.dump(data, j_file, indent=4)

if __name__ == "__main__":
    f_input = sys.argv[1]
    tmp_file = f_input + '.tmp'
    json_file = f_input.replace('.txt', '.json')

    filename = os.path.basename(f_input)
   
    source = get_source_from_fname(filename)
    
    news = construct_json_file(f_input, tmp_file, 5)
    news = load_json(tmp_file)
    #data_cleaning(news)
    news = [ dict(n, **{'source':source, 'class':''} ) for n in news ]
   
    #print(news[0:3])
    write_json_file(json_file, news) 
    os.remove(tmp_file)


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

def construct_csv_file(csv_file, data):
    with open(csv_file, 'w', newline='') as f_csv:
        fieldnames = [ 'class', 'source', 'date', 'title', 'content' ]
        writer = csv.DictWriter(f_csv, fieldnames=fieldnames) 
        writer.writeheader()

        for d in data:
            writer.writerow(d)

def data_cleaning(data):
    # Remove unicode
    unicode_4 = re.compile(r'\\u[A-Za-z0-9]{4}')
    unicode_2 = re.compile(r'\\x[A-Za-z0-9]{2}')
    escape_char = re.compile(r'[\n\t\r]')

    ctr = 0;
    for d in data:
        # Remove escape character
        d['title'] = re.sub(escape_char, '', d['title']).strip()
        d['content'] = re.sub(escape_char, '', d['content']).strip()
        d['date'] = re.sub(escape_char, '', d['date']).strip()


        # Remove unicode
        d['title']   = d['title'].encode('ascii', 'ignore')
        d['title']   = d['title'].decode('utf8')
        #if ctr < 3:
        #    print("[ORIGINAL]")
        #    print(d['content'])

        d['content']   = d['content'].encode('ascii', 'backslashreplace')
        d['content'] = d['content'].decode('utf8')
        d['content'] =  d['content'].replace('\\xa0', ' ') 
        d['content'] = re.sub(unicode_2, '', d['content']).strip()
        d['content'] = re.sub(unicode_4, '', d['content']).strip()

        
        #if ctr < 3:
        #    print("[CONVERTED]")
        #    print(d['content'])
        #    ctr += 1

if __name__ == "__main__":
    f_input = sys.argv[1]
    tmp_file = f_input + '.tmp'
    csv_file = f_input.replace('.txt', '.csv')

    filename = os.path.basename(f_input)
   
    source = get_source_from_fname(filename)
    
    news = construct_json_file(f_input, tmp_file, 5)
    news = load_json(tmp_file)
    data_cleaning(news)
    news = [ dict(n, **{'source':source, 'class':''} ) for n in news ]
   
    #print(news[0:3])
    construct_csv_file(csv_file, news) 

    os.remove(tmp_file)


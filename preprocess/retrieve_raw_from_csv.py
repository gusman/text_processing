import csv
import os
import sys
import json
import re

def construct_list_dict(csv_file):
    json_list = []
    with open(csv_file, newline='') as f_csv:
        fieldnames = [ 'class', 'source', 'date', 'title', 'content' ]
        csv_reader = csv.DictReader(f_csv, fieldnames=fieldnames)
        json_list = [ row for row in csv_reader if 0 < len(row['class']) and len(row['class']) < 5 ]
        for element in json_list:
            if element.get(None):
                del element[None]

    return json_list
                

def get_original_title_and_content(json_list, ori_dir):
    escape_char = re.compile(r'[^\w]')
    unicode_4 = re.compile(r'\\u[A-Za-z0-9]{4}')
    unicode_2 = re.compile(r'\\x[A-Za-z0-9]{2}')


    for d in json_list:
        source = d['source']
        src_file = ori_dir + "/" + source + ".json_tsunami.json"
        #print(src_file)

        d['title_ori'] = ''
        d['content_ori'] = ''
        title = d['title']
        with open(src_file, 'r') as f_src:
            tmp_json = json.load(f_src)


            title = title.replace(' ', '')
            title = re.sub(escape_char, '', title).strip()

            for tmp_d in tmp_json:
                tmp_title = tmp_d['title']
                tmp_title = re.sub(unicode_4, '', tmp_title).strip()
                tmp_title = re.sub(unicode_2, '', tmp_title).strip()
                tmp_title = re.sub(escape_char, '', tmp_title).strip()
                tmp_title = tmp_title.replace(' ', '')
                tmp_title = tmp_title.encode('ascii', 'ignore')
                tmp_title = tmp_title.decode('utf8')

                #print(tmp_title)
                if title in tmp_title:
                    d['content_ori'] = tmp_d['content']
                    d['title_ori'] = tmp_d['title']
            
            if d['title_ori'] == '':
                print("FROM ANOTATED: " + title)
                print("FROM ORI: " + tmp_title)
                print("\n")



    return json_list



if __name__ == "__main__":
    f_in  = sys.argv[1]
    ori_dir = 'C:/Users/dharmapu/Documents/dev/KA-AMSD_src/sample_data/output_20200401_json'
    f_tmp = f_in + ".tmp"
    #print(os.listdir(ori_dir))

    json_list = construct_list_dict(f_in)
    #print(json.dumps(json_list, indent=4))
    json_list = get_original_title_and_content(json_list, ori_dir)
    with open(f_tmp, 'w') as f_tmp:
        json.dump(json_list, f_tmp, indent=4)

    

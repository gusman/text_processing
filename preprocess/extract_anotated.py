import csv
import os
import sys
import json

def get_anotated_only(csv_file):
    json_list = []
    with open(csv_file, newline='') as f_csv:
        fieldnames = [ 'class', 'source', 'date', 'title', 'content' ]
        csv_reader = csv.DictReader(f_csv, fieldnames=fieldnames)
        json_list = [ row for row in csv_reader if 0 < len(row['class']) and len(row['class']) < 5 ]
        for element in json_list:
            if element.get(None):
                del element[None]

    return json_list
                
def write_to_csv(csv_file, json_list):
   with open(csv_file, 'w', newline='') as f_csv:
    fieldnames = [ 'class', 'source', 'date', 'title', 'content' ]
    writer = csv.DictWriter(f_csv, fieldnames=fieldnames) 
    writer.writeheader()

    for d in json_list:
        writer.writerow(d) 

if __name__ == "__main__":
    f_in  = sys.argv[1]
    f_out = f_in.replace('.csv', '') + '_anotated' + '.csv'
   
    json_list = get_anotated_only(f_in)
    #print(json.dumps(json_list, indent=4))
    write_to_csv(f_out, json_list)
    

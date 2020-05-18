import sys
import json

if __name__ == "__main__":
    f_in  = sys.argv[1]
    f_out = f_in.replace(".csv.tmp", ".json")
    #print(os.listdir(ori_dir))

    json_data = []
    with open(f_in, 'r') as f:
        json_data = json.load(f)
    #print(json.dumps(json_list, indent=4))


    json_data = [ dict(d, **{ 'title' : d['title_ori'], 'content' : d['content_ori'] }) for d in json_data ]
    for d in json_data:
        del d['title_ori']
        del d['content_ori']

    json_data = [ d for d in json_data if 0 < len(d['title']) ]

    with open(f_out, 'w') as f:
        json.dump(json_data, f, indent=4)

    

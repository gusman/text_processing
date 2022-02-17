import json

dir_eval_data = '../classification_staging/eval_data_index'

def get_bencana_name(f_path : str) -> str:
    l_bencana = [ 
        'angin_topan', 
        'banjir', 
        'erupsi', 
        'gempa', 
        'karhutla', 
        'kekeringan', 
        'longsor', 
        'tsunami' 
    ]

    for b in l_bencana:
        if b in f_path:
            return b
    
    return None

def get_index(bencana: str, idx: int):
    f_path = f'{dir_eval_data}/{bencana}/{bencana}_eval_index_{idx}.json'
    with open(f_path, 'r') as f:
        b_index = json.load(f)

    return (b_index['train'], b_index['test'])

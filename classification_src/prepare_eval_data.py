import pandas as pd
import os
import sys
import json

from sklearn.model_selection import KFold
from lib import misc

def create_eval_data(df : pd.DataFrame, d_eval : str, bencana : str):
    kf = KFold(n_splits=5, shuffle=True, random_state=0)
    f_out = d_eval + f'/{bencana}'
    
    idx = 1
    for train_index, test_index in kf.split(df):
        f_out_index = f_out + f'_eval_index_{idx}.json'
        b_index = {
            'train' : train_index.tolist(),
            'test'  : test_index.tolist(),
        }
        
        print(f_out_index)
        with open(f_out_index, 'w') as f:
            json.dump(b_index, f)
        idx += 1

if __name__ == '__main__':
    f_in = sys.argv[1]
    d_eval = '../classification_staging/eval_data_index'
    df = pd.read_json(f_in)
    bencana = misc.get_bencana_name(f_in)
    
    d_eval += f'/{bencana}'
    os.makedirs(d_eval, exist_ok=True)
    create_eval_data(df, d_eval, bencana)


import pandas as pd
import sys
from sklearn.metrics import cohen_kappa_score
from os.path import basename

if __name__ == "__main__":
    f_in = sys.argv[1]
    df = pd.read_excel(f_in)
    
    print("-------------------")
    print(basename(f_in))
    label_anot01 = df['label_v01'].to_numpy()
    label_anot02 = df['label_fariq'].to_numpy()
    cohen_score = cohen_kappa_score(label_anot01, label_anot02)
    print(f"TOTAL Data = %d" % len(df.index))
    print(f'COHEN SCORE: %f' % (cohen_score))

    print("-------------------")
    print("LABEL 01 Properties")
    df_label_v01_Y = df[df.label_v01 == 'Y']
    df_label_v01_N = df[df.label_v01 == 'N']
    print(f"Label 01 Y: %d" % len(df_label_v01_Y.index))
    print(f"Label 01 N: %d" % len(df_label_v01_N.index))

    print("-------------------")
    print("LABEL 02 Properties")
    df_label_v02_Y = df[df.label_fariq == 'Y']
    df_label_v02_N = df[df.label_fariq == 'N']
    print(f"Label 02 Y: %d" % len(df_label_v02_Y.index))
    print(f"Label 02 N: %d" % len(df_label_v02_N.index))


    print("-------------------")
    print("LABEL FINAL Properties")
    df_label_v02_Y = df[df.label == 'Y']
    df_label_v02_N = df[df.label == 'N']
    print(f"Label FINAL Y: %d" % len(df_label_v02_Y.index))
    print(f"Label FINAL N: %d" % len(df_label_v02_N.index))


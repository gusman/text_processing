import pandas as pd
import sys

f_in = 'C:\\Users\\dharmapu\\Documents\\personal\\ui\\KA-AMSD_src\\gold_dataset\\gold_data_set_time\\date_gold_standard_v03_fix.xlsx'
df = pd.read_excel(f_in)

print(df[df.id == 'banjir_0477'])

import pandas as pd
from lib.date_measurement import DateMeasurement as DM 
from lib.date_tool import dt_search as ds

DIR_DT_STAGING = '../date_extraction_staging'
DIR_DT_TIMEX = f'{DIR_DT_STAGING}/indo_timex'

if __name__ == '__main__':
    f_tmex = f'{DIR_DT_TIMEX}/indo_timex_result.xlsx'
    f_ref =  f'{DIR_DT_STAGING}/date_actual.xlsx'
    f_text = f'{DIR_DT_STAGING}/date_analysis_text.xlsx'

    df_ref = pd.read_excel(f_ref)
    df_tmx = pd.read_excel(f_tmex)
    df_text = pd.read_excel(f_text)

    df_data = pd.DataFrame()
    df_data = df_ref.copy()
    df_data['tmex'] = df_tmx['date']

    for idx, row in df_data.iterrows():
        article_id = row['id']
        pub_date = df_text[df_text.id == article_id]['date'].values[0]
        final_pub_date = ds.find_dates(pub_date, mmdd=False)
        df_data.loc[idx, 'pub_date'] = final_pub_date


    for index, row in df_data.iterrows():
        
        if "nan".lower() == str(row['date']).lower():
            ref_date = row['pub_date']
        else:  
            ref_date = row['date']

        df_data.loc[index, 'ref_date'] = ref_date

        if "nan".lower() == str(row['tmex']).lower():
            pred_date = row['pub_date']
        else:  
            pred_date = row['tmex']

        df_data.loc[index, 'pred_date'] = pred_date

        l_true = ref_date.split('|')
        l_pred = pred_date.split('|')

        dm = DM(l_true, l_pred)
        df_data.loc[index, 'jc_sim'] = dm.jaccard_simmilarity()
        df_data.loc[index, 'pre'] = dm.precision()
        df_data.loc[index, 'rec'] = dm.recall()
        df_data.loc[index, 'f1'] = dm.f1_score()

    columns = ['jc_sim', 'pre', 'rec', 'f1'] 
    means_list = [ "{:.3f}".format(df_data[c].mean()) for c in columns ]

    last_row = ['MEAN', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']
    last_row = last_row + means_list

    df_tmp = df_data.copy()
    df_tmp.loc[len(df_tmp)] = last_row
    print(df_tmp)

    #f_out = '{DIR_DT_TIMEX}/date-time-timex_rslt.xlsx'
    #df_tmp.to_excel(f_out, index=False)

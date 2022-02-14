import pandas as pd
import re

from lxml import etree as ET
from lib.date_tool import dt_search as ds

DIR_DT_STAGING = '../date_extraction_staging'
DIR_DT_STAGING_TIMEX = f'{DIR_DT_STAGING}/indo_timex'

def create_timeML(article_id, dt, title, text):
    # Create root
    qname = ET.QName("http://www.w3.org/2001/XMLSchema-instance", "noNamespaceSchemaLocation")
    root = ET.Element('TimeML', {qname :'http://timeml.org/timeMLdocs/TimeML_1.2.1.xsd'})

    # Add DOCID Sub-element
    docid = ET.SubElement(root, "DOCID")
    docid.text = article_id

    # Add DCT Sub-element
    dct = ET.SubElement(root, "DCT")
    dct_timex3 = ET.SubElement(dct, "TIMEX3")
    dct_timex3.attrib['tid'] = 't0'
    dct_timex3.attrib['type'] = 'TIME'
    dct_timex3.attrib['value'] = dt
    dct_timex3.attrib['temporalFunction'] = 'false'
    dct_timex3.attrib['functionInDocument'] = 'CREATION_TIME'
    dct_timex3.text = dt

    # Add TITLE
    doctitle = ET.SubElement(root, "TITLE")
    doctitle.text = title

    # Add TEXT
    doctext = ET.SubElement(root, "TEXT")
    doctext.text = text.encode('ascii', 'ignore')

    return ET.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf8').decode('utf-8', 'ignore')

if __name__ == '__main__':
    f_dttm_text_data = f'{DIR_DT_STAGING}/date_analysis_text.xlsx'
    df_dttm = pd.read_excel(f_dttm_text_data)

    f_out_dir = f'{DIR_DT_STAGING_TIMEX}/tml'

    for i, row in df_dttm.iterrows():
        article_id = row['id']
        article_date = row['date']
        article_title = row['title']
        article_content = row['content']
        dt_tml = ds.find_dates(article_date, mmdd=False)

        tml_text = create_timeML(article_id, dt_tml, article_title, article_content)

        tml_text = re.sub(r'<DCT>\n', '<DCT>', tml_text)
        tml_text = re.sub(r'<\/TIMEX3>\n', '</TIMEX3>', tml_text)
        tml_text = re.sub(r'<DCT>[ ]+', '<DCT>', tml_text)
        tml_text = re.sub(r'<\/TIMEX3>[ ]+', '</TIMEX3>', tml_text)
       
        tml_text = re.sub(r'>\n', '>\n\n', tml_text)

        tml_text = re.sub(r'<TEXT>', '<TEXT>\n', tml_text)
        tml_text = re.sub(r'<\/TEXT>', '\n</TEXT>', tml_text)

        tml_text = re.sub('[ ]+<', '<', tml_text)

        tml_text = re.sub(r'\.[ ]+', '.\n\n', tml_text)

        #print(article_id)
        f_name = f_out_dir + "\\" + article_id + ".tml"
        with open(f_name, 'w') as f:
            f.write(tml_text)

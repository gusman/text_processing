import os
from sys import platform

# settings
news_type = 'gempa'
d_delimiter = "\\"

d_cur = os.path.dirname(os.path.realpath(__file__))
d_text_data = d_cur + d_delimiter + ".." + d_delimiter + "data"
f_teks_ori = d_text_data + d_delimiter + "sample_" + news_type + ".xlsx"

d_preprocess = d_cur + d_delimiter + ".." + d_delimiter + ".." + d_delimiter + "preprocess"
preprocess_path = os.path.realpath(d_cur + d_delimiter + ".." + d_delimiter + ".." + d_delimiter + "preprocess")

if platform == "win32":
    d_news_text = 'C:\\Users\\dharmapu\\documents\\personal\\ui\\KA-AMSD_src\\final_data\\hasil-scraping\\complete'
else:
    d_news_text = 'C:\\Users\\dharmapu\\documents\\personal\\ui\\KA-AMSD_src\\final_data\\hasil-scraping\\complete'

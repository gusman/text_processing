import json
import re
import os
import sys

class FilterNews:
    min_str_len = 5
    news = []
    flt_news = []
    keywords = {
        'angin_topan'   : [ 'badai', 'puting beliung', 'angin topan', 'tornado', 'angin kencang' ],
        'banjir'        : [ 'banjir' ],
        'gempa'         : [ 'gempa', 'tektonik' ],
        'gunung_api'    : [ 'vulkanik', 'erupsi', 'letusan', 'awan panas', 'lava' ],
        'karhutla'      : [ 'kebakaran hutan', 'kebakaran lahan', 'titik panas', 'karhutla' ],
        'kekeringan'    : [ 'kekeringan' ],
        'longsor'       : [ 'longsor' ],
        'tsunami'       : [ 'tsunami' ]
    }

    def __init__(self, disaster_type, fname):
        self.disaster_type = disaster_type
        self.fullpath = os.path.abspath(fname)
        self.dirpath  = os.path.dirname(self.fullpath)
        self.filename = os.path.basename(self.fullpath)
       
    def __filter_by_keywords(self, data, source):
        ret = False
        keywords = self.keywords[self.disaster_type];
        
        if data['title'] and data['content'] \
            and self.min_str_len < len(data['title']) \
            and self.min_str_len < len(data['content']):

            for key in keywords:

                    result = re.search(key, data['title'], re.IGNORECASE)
                    if None != result:
                       ret = True 

                    result = re.search(key, data['content'], re.IGNORECASE)
                    if None != result:
                       ret = True 

        if True == ret:
            data['source'] = source
        return ret

    def load_news(self):
        with open(self.fullpath, 'r') as f:
            self.news = json.load(f)

    def filter_news(self):
        self.flt_news = [ n for n in self.news if True == self.__filter_by_keywords(n, self.filename) ]

    def save_news(self):
        out_path = self.dirpath + "/flt_" + self.disaster_type + "_" + self.filename
        with open(out_path, 'w') as f:
            json.dump(self.flt_news, f, indent=2)


if __name__ == "__main__":
    disaster_type = sys.argv[1]
    fname = sys.argv[2]
    
    FltNews = FilterNews(disaster_type, fname)
    FltNews.load_news()
    FltNews.filter_news()
    FltNews.save_news()


import re

month_dict = {
    'jan' : '01',
    'feb' : '02',
    'peb' : '02',
    'mar' : '03',
    'apr' : '04',
    'may' : '05',
    'mai' : '05',
    'mei' : '05',
    'jun' : '06',
    'jul' : '07',
    'agu' : '08',
    'aug' : '08',
    'sep' : '09',
    'oct' : '10',
    'okt' : '10',
    'nov' : '11',
    'nop' : '11',
    'des' : '12',
    'dec' : '12',
}

def get_month_number(text):
    ret = ''
    for k, v in month_dict.items():
        if text.lower().startswith(k):
            ret = v
            break
    return ret


def test(rslt):
    # Only join result by ' '
    print(rslt)
    return [' '.join(e) for e in rslt ]

def date_dd_MM_yyyy(rslt):
    ret = []
    for e in rslt:
        date = '%02d' % int(e[0])
        month = get_month_number(e[1])
        year = e[2] + e[3]
        ret.append(f'{year}-{month}-{date}')
    return ret

def date_MM_dd_yyyy(rslt):
    ret = []
    for e in rslt:
        month = get_month_number(e[0])
        date = '%02d' % int(e[1])
        year = e[2] + e[3]
        ret.append(f'{year}-{month}-{date}')
    return ret

def date_yyyy_mm_dd(rslt):
    ret = []
    for e in rslt:
        year = e[0] + e[1]
        month = '%02d' % int(e[2])
        date = '%02d' % int(e[3])
        ret.append(f'{year}-{month}-{date}')
    return ret

def date_dd_mm_yyyy(rslt):
    ret = []
    for e in rslt:
        date = '%02d' % int(e[0])
        month = '%02d' % int(e[1])
        year = e[2] + e[3]
        ret.append(f'{year}-{month}-{date}')
    return ret

def date_dd_mm(rslt):
    ret = []
    for e in rslt:
        date = '%02d' % int(e[0])
        month = '%02d' % int(e[1])
        ret.append(f'{month}-{date}')
    return ret

def date_dd_MM(rslt):
    ret = []
    for e in rslt:
        date = '%02d' % int(e[0])
        month = get_month_number(e[1])
        ret.append(f'{month}-{date}')
    return ret



class RegexMap:
    def __init__(self, id, r_pattern, func):
        self.id = id
        self.r_pattern = r_pattern
        self.func = func

class RegexResult:
    def __init__(self, l_text, func):
        self.l_text = l_text
        self.func = func
        
class DateSearch:
    l_regex_map_yyymmdd = [
        # 01 Januari 2020 (inc date and month single digit)
        RegexMap('r01', r'([0123]?[0-9]) ([A-Za-z]+) (19|20)([0-9]{2})', date_dd_MM_yyyy),

        # Januari 1, 2020 (inc date and month single digit)
        RegexMap('r02', r'([A-Za-z]+) ([0123]?[0-9]), (19|20)([0-9]{2})', date_MM_dd_yyyy),
       
        # 01-12-2020 (inc date and month single digit)
        RegexMap('r03', r'([0123]?[0-9])[\\\/\- ]([01]?[0-9])[\\\/\- ](19|20)([0-9]{2})', date_dd_mm_yyyy),
        
        # 01/12/2020 (inc date and month single digit)
        #RegexMap('r04', r'([0123]?[0-9])\/([01]?[0-9])\/(19|20)([0-9]{2})', date_dd_mm_yyyy),

        # 01\12\2020 (inc date and month single digit)
        #RegexMap('r05', r'([0123]?[0-9])\\([01]?[0-9])\\(19|20[0-9]{2})', date_dd_mm_yyyy),
        
        # 2020-01-01 (inc date and month single digit)
        RegexMap('r06', r'(19|20)([0-9]{2})[\\\/\- ]([01]?[0-9])[\\\/\- ]([0123]?[0-9])', date_yyyy_mm_dd),
        
        # 2020/01/01 (inc date and month single digit)
        #RegexMap('r07', r'(19|20[0-9]{2})\/([01]?[0-9])\/([0123]?[0-9])', date_yyyy_mm_dd),

        # 2020\01\01 (inc date and month single digit)
        #RegexMap('r08', r'(19|20[0-9]{2})\\([01]?[0-9])\\([0123]?[0-9])', date_yyyy_mm_dd),
    ]

    l_regex_map_mmdd = [
        # 01/12 (inc date and month single digit)
        RegexMap('r09', r'[\s(\.\,]([0123]?[0-9])[\\\/]([01]?[0-9])', date_dd_mm),
        
        # 01 Jan (inc date and month single digit)
        RegexMap('r10', r'[\s(\.\,]([0123]?[0-9])[\- ](januari|februari|pebruari|maret|april|may|mai|mey|juni|juli|agustus|september|oktober|november|nopember|desember)', date_dd_MM),
    ]

    l_result = []
   
    def __proc_result(self):
        r_list = []
        for e in self.l_result:
            r_list.extend(e.func(e.l_text))
            
        return '|'.join(r_list)

    def find_dates(self, text, mmdd = True):
        self.l_result = []

        for re_map in self.l_regex_map_yyymmdd:
            result = re.findall(re_map.r_pattern, text, re.I)
            if result:
                 self.l_result.append(RegexResult(result, re_map.func))

        if True == mmdd:
            for re_map in self.l_regex_map_mmdd:
                result = re.findall(re_map.r_pattern, text, re.I)
                if result:
                    self.l_result.append(RegexResult(result, re_map.func))

                    
        return self.__proc_result()


# Final object
dt_search = DateSearch()

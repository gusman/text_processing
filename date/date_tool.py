import pandas as pd
import sys
import re

def test(rslt):
    # Only join result by ' '
    return [' '.join(e) for e in rslt ]

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
    l_regex_map = [
        # 01 Januari 2020 (inc date single digit)
        RegexMap('r01', r'([0123]?[0-9]) ([A-Za-z]+) (19|20[0-9]{2})', test),

        # Januari 1, 2020 (inc date single digit)
        RegexMap('r02', r'([A-Za-z]+) ([0123]?[0-9]), (19|20[0-9]{2})', test),

        # 2020-01-01 (inc date and month single digit)
        RegexMap('r03', r'(19|20[0-9]{2})-([01]?[0-9])-([0123]?[0-9])', test),

        # 2020/01/01 (inc date and month single digit)
        RegexMap('r04', r'(19|20[0-9]{2})/([01]?[0-9])/([0123]?[0-9])', test),

        # 2020\01\01 (inc date and month single digit)
        RegexMap('r05', r'(19|20[0-9]{2})\\([01]?[0-9])\\([0123]?[0-9])', test),
    ]

    l_result = []
   
    def __proc_result(self):
        r_list = []
        for e in self.l_result:
            r_list.extend(e.func(e.l_text))
            
        return '|'.join(r_list)

    def find_date(self, text):
        for re_map in self.l_regex_map:
            result = re.findall(re_map.r_pattern, text, re.I)
            if result:
                 self.l_result.append(RegexResult(result, re_map.func))
                    
        return self.__proc_result()


# Final object
dt_search = DateSearch()
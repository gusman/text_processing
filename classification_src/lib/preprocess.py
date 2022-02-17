import sys
import json
import re
from nltk import word_tokenize
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

def clean_specific_char(text):
    pattern01 = re.compile(r"\\u00a0")
    pattern02 = re.compile(r"\\xa0")
    pattern03 = re.compile(r"\\xad")
    pattern04 = re.compile(r"\\")
    pattern05 = re.compile(r"\/")
    pattern06 = re.compile(r"\(")
    pattern07 = re.compile(r"\)")
    pattern08 = re.compile(r"\,")
    pattern09 = re.compile(r"\.")

    text = re.sub(pattern01, ' ', text).strip()
    text = re.sub(pattern02, ' ', text).strip()
    text = re.sub(pattern03, ' ', text).strip()
    text = re.sub(pattern04, ' ', text).strip()
    text = re.sub(pattern05, ' ', text).strip()
    text = re.sub(pattern06, ' ', text).strip()
    text = re.sub(pattern07, ' ', text).strip()
    text = re.sub(pattern08, ' ', text).strip()
    text = re.sub(pattern09, ' ', text).strip()
    return text

def clean_number(text):
    number = re.compile(r"\d")
    text = re.sub(number, '', text).strip()
    return text

def clean_unicode_char(text):
    unicode_4 = re.compile(r"\\u[A-Za-z0-9]{4}")
    unicode_2 = re.compile(r"\\x[A-Za-z0-9]{2}")
    text = re.sub(unicode_4, ' ', text).strip()
    text = re.sub(unicode_2, ' ', text).strip()
    return text

def clean_escape_char(text):
    escape_char = re.compile(r"[\n\t\r]")
    text = re.sub(escape_char, ' ', text).strip()
    return text

def add_space_after_period_comma(text):
    regex = re.compile(r"(?<=[.,])(?=[^\s0-9])")
    text = re.sub(regex, ' ', text).strip()
    return text

def clean_specific_words(text):
    words_1 = '(adsbygoogle = window.adsbygoogle || []).push({});'
    words_2 = '\nHome'
    text = text.replace(words_1, '').strip()
    text = text.replace(words_2, '').strip()
    return text

def clean_links_text(text):
    links_1 = re.compile(r"([Bb][Aa][Cc][Aa])([^.{}]*)(?<!\")")
    links_2 = re.compile(r"\\u2022([^.{}]*)(?<!\")")
    links_3 = re.compile(r"([Ll][Ii][Hh][Aa][Tt]):([^.{}]*)(?<!\")")
    links_4 = re.compile(r"([Bb][Ee][Rr][Ii][Tt][Aa] [Ll][Aa][Ii][Nn])([^.{}]*)(?<!\")")
    
    text = re.sub(links_1, ' ', text).strip()
    text = re.sub(links_2, ' ', text).strip()
    text = re.sub(links_3, ' ', text).strip()
    text = re.sub(links_4, ' ', text).strip()
    return text

def clean_convertion(text):
    text = text.encode('ascii', 'backslashreplace')
    text = text.decode('utf8')
    return text
    
def clean_text(text):
    text = clean_unicode_char(text)
    text = clean_specific_words(text)
    text = clean_specific_char(text)
    text = clean_escape_char(text)
    text = clean_number(text)
    text = add_space_after_period_comma(text)
    return text

def stem_text(text):
    stemmer = StemmerFactory().create_stemmer()
    return stemmer.stem(text)

def rem_stop_words(text):
    sw_rem = StopWordRemoverFactory().create_stop_word_remover()
    return sw_rem.remove(text)

def clean_up(json_data):
    for d in json_data:
        d['title'] = d['title'].encode('ascii', 'backslashreplace')
        d['title'] = d['title'].decode('utf8')
        d['title'] = clean_text(d['title'])
        
        d['content'] = d['content'].encode('ascii', 'backslashreplace')
        d['content'] = d['content'].decode('utf8')
        d['content'] = clean_text(d['content'])
        
        d['date'] = d['date'].encode('ascii', 'backslashreplace')
        d['date'] = d['date'].decode('utf8')
        d['date'] = clean_text(d['date'])
    return json_data

def preprocess_lower(d):
    d['t_lower'] = d['title'].lower()
    d['c_lower'] = d['content'].lower()
    d['tc_lower'] = d['t_lower'] + '. ' + d['c_lower']
    return d

def preprocess_sw_rem(d):
    d['t_swrem'] = rem_stop_words(d['t_lower'])
    d['c_swrem'] = rem_stop_words(d['c_lower'])
    d['tc_swrem'] = d['t_swrem'] + '. ' + d['c_swrem']
    return d

def preprocess_stem(d):
    d['t_stem'] = stem_text(d['t_lower'])
    d['c_stem'] = stem_text(d['c_lower'])
    d['tc_stem'] = d['t_stem'] + '. ' + d['c_stem']
    return d

def preprocess_swrem_stem(d):
    d['t_swrem_stem'] = stem_text(d['t_swrem'])
    d['c_swrem_stem'] = stem_text(d['c_swrem'])
    d['tc_swrem_stem'] = d['t_swrem_stem'] + '. ' + d['c_swrem_stem']
    return d



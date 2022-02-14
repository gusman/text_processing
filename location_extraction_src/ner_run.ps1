$ner_st = '.\ner_proc_st_keywords.py'
$ner_words = '.\ner_proc_w_tokens.py'

Start-Process py -ArgumentList $ner_st
Start-Process py -ArgumentList $ner_words

$gztr_1 = '.\gazetteer_search_1.py'
$gztr_2 = '.\gazetteer_search_2.py'
$gztr_3 = '.\gazetteer_search_3.py'

$ner_result = '..\location_extraction_staging\ner_output\ner_out_w_tokens.xlsx'

Start-Process py -ArgumentList $gztr_1, $ner_result
Start-Process py -ArgumentList $gztr_2, $ner_result
Start-Process py -ArgumentList $gztr_3, $ner_result

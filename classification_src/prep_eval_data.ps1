$pyscript = '.\prepare_eval_data.py'
$preproc_dir = '..\classification_staging\preproc_text'

$preproc_text_angin_topan = $preproc_dir + '\' + 'angin_topan_text_label_preproc.json'
$preproc_text_banjir = $preproc_dir + '\' + 'banjir_text_label_preproc.json'
$preproc_text_erupsi = $preproc_dir + '\' + 'erupsi_text_label_preproc.json'
$preproc_text_gempa = $preproc_dir + '\' + 'gempa_text_label_preproc.json'
$preproc_text_karhutla = $preproc_dir + '\' + 'karhutla_text_label_preproc.json'
$preproc_text_kekeringan = $preproc_dir + '\' + 'kekeringan_text_label_preproc.json'
$preproc_text_longsor = $preproc_dir + '\' + 'longsor_text_label_preproc.json'
$preproc_text_tsunami = $preproc_dir + '\' + 'tsunami_text_label_preproc.json'

py $pyscript $preproc_text_angin_topan
py $pyscript $preproc_text_banjir
py $pyscript $preproc_text_erupsi
py $pyscript $preproc_text_gempa
py $pyscript $preproc_text_karhutla
py $pyscript $preproc_text_kekeringan
py $pyscript $preproc_text_longsor
py $pyscript $preproc_text_tsunami

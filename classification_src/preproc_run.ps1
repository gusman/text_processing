$pyscript = '.\preproc_ano_file.py'
$log_dir = '..\classification_staging\preproc_log'
$out_dir = '..\classification_staging\preproc_text'

$label_text_dir = '..\classification_staging\labeled_text'

$label_text_angin_topan = $label_text_dir + '\' + 'angin_topan_text_label.xlsx'
$label_text_banjir = $label_text_dir + '\' + 'banjir_text_label.xlsx'
$label_text_erupsi = $label_text_dir + '\' + 'erupsi_text_label.xlsx'
$label_text_gempa = $label_text_dir + '\' + 'gempa_text_label.xlsx'
$label_text_karhutla = $label_text_dir + '\' + 'karhutla_text_label.xlsx'
$label_text_kekeringan = $label_text_dir + '\' + 'kekeringan_text_label.xlsx'
$label_text_longsor = $label_text_dir + '\' + 'longsor_text_label.xlsx'
$label_text_tsunami = $label_text_dir + '\' + 'tsunami_text_label.xlsx'

ls $pyscript
ls $log_dir
ls $out_dir

ls $label_text_angin_topan
ls $label_text_banjir
ls $label_text_erupsi
ls $label_text_gempa
ls $label_text_karhutla
ls $label_text_kekeringan 
ls $label_text_longsor
ls $label_text_tsunami

#Start-Process py -ArgumentList $pyscript, $label_text_angin_topan, $out_dir, $log_dir 
#Start-Process py -ArgumentList $pyscript, $label_text_banjir, $out_dir, $log_dir 
#Start-Process py -ArgumentList $pyscript, $label_text_erupsi, $out_dir, $log_dir 
#Start-Process py -ArgumentList $pyscript, $label_text_gempa, $out_dir, $log_dir 
Start-Process py -ArgumentList $pyscript, $label_text_karhutla, $out_dir, $log_dir 
#Start-Process py -ArgumentList $pyscript, $label_text_kekeringan, $out_dir, $log_dir 
Start-Process py -ArgumentList $pyscript, $label_text_longsor, $out_dir, $log_dir 
#Start-Process py -ArgumentList $pyscript, $label_text_tsunami, $out_dir, $log_dir 

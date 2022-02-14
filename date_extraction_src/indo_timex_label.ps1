$dir_indotimex = '.\IndoTimex'
$pyscript = '.\TimexExtraction.py'
$dir_tml_input  = '..\..\date_extraction_staging\indo_timex\tml'
$dir_tml_output = '..\..\\date_extraction_staging\indo_timex\indo_timex_label'

cd $dir_indotimex

$files = Get-ChildItem $dir_tml_input 

foreach ($f in $files) {
    python $pyscript $dir_tml_input\$f -o $dir_tml_output\$f
}

cd ..

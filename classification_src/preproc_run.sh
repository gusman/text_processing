DIR_PREPROC=../classification_staging/preproc_text
DIR_LOG=../classification_staging/preproc_log
DIR_LABELED_TEXT=../classification_staging/labeled_text

PY_SCRIPT=./preproc_ano_file.py

# Run the sript and spawn the process in backround
for f in $DIR_LABELED_TEXT/*.xlsx; do
    python $PY_SCRIPT $f $DIR_PREPROC $DIR_LOG &
done


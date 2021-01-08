SET STANFORD_NER=C:\Users\dharmapu\Documents\personal\ui\KA-AMSD_src\src\stanford-ner-2020-11-17\stanford-ner.jar
SET PROP=C:\Users\dharmapu\Documents\personal\ui\KA-AMSD_src\src\ner-model\build_20k_mdee.prop

java -Xmx8192m -cp %STANFORD_NER% edu.stanford.nlp.ie.crf.CRFClassifier -prop %PROP%

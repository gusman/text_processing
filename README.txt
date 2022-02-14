Folder description:
- anotated_data
 > contains anotated data

- classification_src
 > Source code that needed for classification analysis

- classification_staging
 > Staging data that for classification analysis
 > eval_data_index: contains index data after K-Fold reshufling
 > preproc_text: contains data after preprocessing and label
 > labeled_text: contains selected anotated data for classification analysis   

- date_extraction_src
 > Source code date and time extraction analysis

- date_extraction_staging
 > Contains data for date and time extraction analysis
 > indo_timex: specific data for date_extraction using indo_timex method

- location_extraction_src
 > Source for location extraction analysis

- location_extraction_staging
 > Contains data for location extraction analysis
 > ner_output: location data extracted using ner
 > gazetteer_output: location data of adm1, adm2, and adm3 based on ner output
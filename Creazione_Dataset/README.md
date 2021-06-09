# CREAZIONE DATASET

In questa cartella sono contentenuti gli script per estrarre le frasi dal dataset "vatpub" e formare la parte non perturbata del dataset.

## sentences_extraction.py
E' uno script che prende il testo diviso in paragrafi dal dataset e lo divide in singole frasi. Tutte le frasi, divise per numero di documento, sono salvate in un file di nome ```senteces.json```. <br>
**Attenzione:** prima di eseguire lo script è necessario settare la directory contentente il dataset all'interno dello script stesso. Il path deve essere quello della cartella contentente tutti i file ```xxxx.json```.
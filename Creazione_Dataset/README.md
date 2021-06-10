# Creazione dataset

In questa cartella sono contentenuti gli script per estrarre le frasi dal dataset "vatpub" e formare la parte non perturbata del dataset.

## sentences_extraction.py
E' uno script che prende il testo diviso in paragrafi dal dataset e lo divide in singole frasi. Tutte le frasi, divise per numero di documento, sono salvate in un file di nome ```sentences.json```. <br>
**Attenzione:** prima di eseguire lo script è necessario settare la directory contentente il dataset all'interno dello script stesso. Il path deve essere quello della cartella contentente tutti i file ```xxxx.json```.

## dataset_creation.py
E' uno script che prende le frasi estratte in ```sentences.json``` e le suddivide in minifrasi da 50 caratteri massimo. Questo limite è dovuto al fatto che le frasi devono essere ulteriormente elaborate per essere date in pasto a NEMATUS. Tutte le frasi ottenute vengon dumpate su ```extracted.json```.
**Attenzione**: l'esecuzione è abbastanza lunghetta
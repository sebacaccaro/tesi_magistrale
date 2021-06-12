# NEMATUS
In questa cartella è presente il dockerfile per nematus. Tutta la doc (risicata) su nemauts è presente [qui](https://github.com/EdinburghNLP/nematus).

Nematus può essere eseguito all'interno di docker.
Per creare la dockerimage, seguire i seguenti comandi:

- `git clone https://github.com/EdinburghNLP/nematus`
- ```rm nematus/Dockerfile.cpu```
- ```cp Dockerfile.cpu nematus```
- `cd nematus`
- `docker build -t nematus-docker -f Dockerfile.cpu .`

Per far partire un container nella directory corrente con l'immagine appena creata, usare il seguente comando:

```docker run -v `pwd`:/playground -it nematus-docker```

All'interno del container, esegure,

```nematus.py [options]```
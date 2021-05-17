from nltk import word_tokenize

# TODO Aggiungere accapo finali

inputfile = "input.txt"

# Leggo un file in input e mergio le linee
with open("input.txt") as f:
    lines = f.readlines()

lines = "".join(lines)

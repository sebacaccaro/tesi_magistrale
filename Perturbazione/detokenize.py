from os import remove
from nltk.tokenize.treebank import TreebankWordDetokenizer
from nltk import word_tokenize


def detokenize(input):
    output = TreebankWordDetokenizer().detokenize(input)
    output = output.replace(" , ", ", ")
    output = output.replace(" ' ", "'")
    output = output.replace(" ’ ", "’")
    output = output.replace(" ’", "’")
    output = output.replace(" . ", ". ")
    output = output.replace(" : ", ": ")
    output = output.replace(" ; ", "; ")
    return output

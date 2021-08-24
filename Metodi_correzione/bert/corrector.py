from nltk.tokenize.treebank import TreebankWordDetokenizer
from bert_filler import Filler
from nltk import word_tokenize


def detokenize(input: list):
    output = TreebankWordDetokenizer().detokenize(input)
    output = output.replace(" , ", ", ")
    output = output.replace(" ' ", "'")
    output = output.replace(" ’ ", "’")
    output = output.replace(" ’", "’")
    output = output.replace(" . ", ". ")
    output = output.replace(" : ", ": ")
    output = output.replace(" ; ", "; ")
    return output


class Corrector:

    def __init__(self, dict_path: str, bert_filler: Filler) -> None:
        self.log = False
        self.filler = bert_filler
        self.vocabulary = set()
        with open(dict_path, 'r', encoding='utf-8') as f:
            for line in f:
                self.vocabulary.add(line.strip())

    def enable_log(self) -> None:
        self.log = True

    def isError(self, word: str) -> bool:
        return word.lower() not in self.vocabulary

    def correct(self, sentence):
        tokens = word_tokenize(sentence)
        for i in range(len(tokens)):
            token = tokens[i]
            if self.isError(token):
                sentence = detokenize(
                    [*tokens[:i], self.filler.FILL_STR, *tokens[i+1:]])
                correction = self.filler.guess(sentence, token)
                tokens[i] = correction
        sentence = detokenize(tokens)
        return sentence

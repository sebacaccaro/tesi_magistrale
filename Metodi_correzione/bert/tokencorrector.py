from nltk.tokenize.treebank import TreebankWordDetokenizer
from bert_filler import Filler
from nltk import word_tokenize
import string
import re
from Levenshtein import distance


def detokenize(input: list):
    output = TreebankWordDetokenizer().detokenize(input)
    output = output.replace(" , ", ", ")
    output = output.replace(" ' ", "'")
    output = output.replace("' ", "'")
    output = output.replace(" ’ ", "’")
    output = output.replace(" ’", "’")
    output = output.replace(" . ", ". ")
    output = output.replace(" : ", ": ")
    output = output.replace(" ; ", "; ")
    return output


def mod_tokenize(sentence):
    tokens = word_tokenize(sentence)
    modTokens = []
    for token in tokens:
        if "'" in token:
            divided = [str.strip(t)
                       for t in re.split("(')",  token) if t != '']
            modTokens.extend(divided)
        else:
            modTokens.append(token)
    return modTokens


class TokenCorrector:

    def __init__(self, dict_path: str, bert_filler: Filler) -> None:
        self.log = False
        self.filler = bert_filler
        self.vocabulary = set()
        with open(dict_path, 'r', encoding='utf-8') as f:
            for line in f:
                self.vocabulary.add(line.strip())
        for punct in string.punctuation:
            self.vocabulary.add(punct)

    def enable_log(self) -> None:
        self.log = True

    def isError(self, words: str, index: int) -> bool:
        if len(words[index]) <= 1:
            return False
        if words[index].lower() not in self.vocabulary:
            # Checking if error word is a word with apostrophe
            if index + 1 < len(words) and words[index+1] == "'":
                word = words[index]
                possibleFull = [
                    word.lower() + c for c in ["a", "e", "i", "o", "u"]]
                return not any([p in self.vocabulary for p in possibleFull])
            return True
        return False

    def isCorrectionCloseEnough(self, original, correction):
        editDistance = distance(original, correction)
        if len(original) > 10:
            if editDistance < 5:
                return True
        elif len(original) > 5:
            if editDistance < 4:
                return True
        else:
            if editDistance < 3:
                return True
        return False

    def correct(self, sentence):
        tokens = mod_tokenize(sentence)
        for i in range(len(tokens)):
            token = tokens[i]
            if self.isError(tokens, i):
                sentence = detokenize(
                    [*tokens[:i], self.filler.FILL_STR, *tokens[i+1:]])
                correction = self.filler.guess(sentence, token)
                if (self.isCorrectionCloseEnough(tokens[i], correction)):
                    tokens[i] = correction
        sentence = detokenize(tokens)
        return sentence

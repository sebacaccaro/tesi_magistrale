from utils import probability_boolean, find_all
from itertools import chain
from nltk import word_tokenize
from random import randint, shuffle
from nltk.tokenize.treebank import TreebankWordDetokenizer


class Pipeline:
    modules = []

    def addModule(self, module):
        self.modules.append(module)

    def feedInput(self, tokens):
        self.input = tokens

    def run(self, input):
        for module in self.modules:
            input = module.apply(input)
        return input


class PerturbationModule:
    function = None
    token_grouping = None
    probability = None

    def group(self, tokens):
        padded = [*tokens, *[""] *
                  (self.token_grouping - (len(tokens) % self.token_grouping))]
        grouped = [padded[i: i+self.token_grouping]
                   for i in range(0, len(padded)-self.token_grouping, self.token_grouping)]
        return grouped

    def __init__(self, perturbation_function, token_grouping, probability):
        self.perturbation_function = perturbation_function
        self.token_grouping = token_grouping
        self. probability = probability

    def apply(self, tokens):
        perturbed_list = [self.perturbation_function(t) if probability_boolean(
            self.probability) else t for t in self.group(tokens)]
        return list(chain.from_iterable(perturbed_list))


class TokenizerModule:
    def apply(self, input):
        return word_tokenize(input)


class DetokenizerModule:
    def apply(self, input):
        return TreebankWordDetokenizer().detokenize(input)


# TODO possibile non segmentare l'intera parola, ma dividerla in pezzettoni
# e segmentarne solo alcuni
def split(token):
    return " ".join([char for char in token])


def split_tokens(list_of_tokens):
    return [split(t) for t in list_of_tokens]


def SplitModuleGenerator(probability):
    return PerturbationModule(
        perturbation_function=split_tokens,
        token_grouping=1,
        probability=probability
    )

# TODO si potrebbe complicare andando a scegliere un sequenza di char
# che non sia la prima, ma va bene anche cosi


""" def replaceChars(token, findChar, replaceChars):
    return token.replace(findChar, replaceChars)


def replaceChars_Tokens(tokens, findChar, replaceChar):
    return [replaceChars(t, findChar, replaceChar) for t in tokens]


def CharsSubModule(probability, findChars, replaceChars):
    return PerturbationModule(
        perturbation_function=lambda tokens: replaceChars_Tokens(
            tokens, findChars, replaceChars),
        token_grouping=1,
        probability=probability
    ) """


def AddPunctuationModule(probability, punctChar):
    return PerturbationModule(
        perturbation_function=lambda tokens: [*tokens, punctChar],
        token_grouping=1,
        probability=probability
    )


def MergeWordHyphenModule(probability):
    return PerturbationModule(
        perturbation_function=lambda tokens: [f"{tokens[0]}-{tokens[1]}"],
        token_grouping=2,
        probability=probability
    )


def addComma(token, punctChar):
    orginal_length = len(token)
    comma_pointer = 0
    if len(token) > 1:
        while comma_pointer < orginal_length:
            comma_pointer += randint(1, orginal_length-1)
            if comma_pointer < orginal_length:
                token = token[:comma_pointer] + \
                    punctChar + token[comma_pointer:]
                comma_pointer += 1
    return token


def SplitWithCommaModule(probability, punctChar):
    return PerturbationModule(
        perturbation_function=lambda tokens: [
            addComma(t, punctChar) for t in tokens],
        token_grouping=1,
        probability=probability
    )


def replaceChars(token, subMatrix):
    appliable = {k: subMatrix[k] for k in subMatrix.keys() if k in token}
    subCandidates = list(appliable.keys())
    shuffle(subCandidates)
    tokenBitMask = [0 for char in token]
    for sub in subCandidates:
        subProb = appliable[sub]["prob"]
        subWith = appliable[sub]["sub"]
        for start in find_all(token, sub):
            if sum(tokenBitMask[start:start+len(sub)]) == 0 and probability_boolean(subProb):
                token = token[:start] + subWith + token[start+len(sub):]
                tokenBitMask = tokenBitMask[:start] + \
                    [1 for c in subWith] + tokenBitMask[start+len(sub):]
    return token


def replaceChars_Tokens(tokens, subMatrix):
    return [replaceChars(t, subMatrix) for t in tokens]


def CharsSubModule(subMatrix, probability=1):
    return PerturbationModule(
        perturbation_function=lambda tokens: replaceChars_Tokens(
            tokens, subMatrix),
        token_grouping=1,
        probability=probability
    )

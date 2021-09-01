import json
import re
from typing import Match
from utils import cleanOutput, string_subtract
from bert_filler import Filler
from Levenshtein import distance


examples = ["millenario della s u a nascita,, che si celebra in",
            "d i l e t t i membri, d e l l a vostra Associazione,. che",
            "Diamo a l bnrnbini un fuluro di pace'!",
            "a Romj per iniziare id loro cammino sulle m c ni o r i e",
            "da Dio e o,gni altro tipo di u n i o, n e.",
            "guLdat0 d ui l l a fedc', nlal bircondare di affettuosn.",
            "sjfferenze, r' tiitto il resto. Mg. a n c h  .' cra Mkdonna",
            "avvenimento, ecclesiale che rester\u00e0. per s e m p r e nel",
            "conservo u n ricordo gratD, e, bPneftco dcl iiostro",
            "coinvolsero ogni uomo e o g n i donna, procurando.",
            "coinvolsero ogni uomo e ogni donna, p r o c u r a n d o."]


class SplitCorrector:

    # Regex per trovare le parole frammentate
    split_reg = r'(?:\s|^)(\w(?:\W?\s\w{1,2}){3,})(?:\W|\s|$)'
    max_accettable_distance = 4

    def __init__(self, vocabulary: set, filler: Filler) -> None:
        self.vocabulary = vocabulary
        self.filler = filler

    def __isMatchCorrect(self, matchedString):
        """ 
        Checks if the matched string is a correct match
        Basically, the function checks if the number of two char sequence is too
        high compared to the number of single char sequences
        """
        just_char_str = re.sub(r'[^\w\s]+', '', matchedString).strip()
        # Regexes matching one and two char words inside the matched string
        singles = len(re.findall(r'(?=(?:^|\s)\w(?:$|\s))', just_char_str))
        doubles = len(re.findall(r'(?=(?:^|\s)\w\w(?:$|\s))', just_char_str))
        return singles > doubles

    def __replace_match(self, sentence: str, match: Match, insertion: str, offset: int):
        start, end = match.start(1) + offset, match.end(1)+offset
        sentence = sentence[:start] + " " + insertion + " " + sentence[end:]
        sentence = cleanOutput(sentence)
        return sentence

    def __fix_with_vocab(self, sentence: str, match: Match, offset: int):
        segment = match.group(1).replace(" ", "")
        if segment in self.vocabulary:
            return self.__replace_match(sentence, match, segment, offset)
        return None

    def __fix_with_filler(self, sentence, match, offset):
        """ 
        Ci sono vari casi da considerare:
        - La parola viene identificata e corretta perchè è semplicemente una parola spezzettata
            Ex. d i l e t t i membri, d e l l a vostra Associazione
        - La regex comprende due parole. Bert potrebbe indovinarne una. Si potrebbe pensare di fare
          una sottrazione e vedere se il restante è una parola buona.
            Ex. coinvolsero ogni uomo e o g n i donna, procurando.
        - No clue > Sad
        """
        segment = match.group(1).replace(" ", "")
        maskedSentence = self.__replace_match(
            sentence, match, self.filler.FILL_STR, offset)
        guessed_word = self.filler.guess(maskedSentence, segment)

        left_word, right_word = string_subtract(segment, guessed_word)
        if left_word:
            return self.__replace_match(sentence, match, left_word + " " + right_word, offset)

        if distance(guessed_word, segment) < self.max_accettable_distance:
            return self.__replace_match(sentence, match, guessed_word, offset)
        return None

    def __fix_match(self, sentence, match, offset):
        return self.__fix_with_vocab(sentence, match, offset) or self.__fix_with_filler(sentence, match, offset) or sentence

    def correct(self, sentence):
        matches = re.finditer(self.split_reg, sentence)
        offset = 0
        for match in matches:
            if self.__isMatchCorrect(match.group(1)):
                original_sentence = sentence
                sentence = self.__fix_match(original_sentence, match, offset)
                offset = len(sentence)-len(original_sentence)
        return sentence


vocabulary = set()
with open("lexicon.txt", 'r', encoding='utf-8') as f:
    for line in f:
        vocabulary.add(line.strip())

filler = Filler()

splc = SplitCorrector(vocabulary, filler)

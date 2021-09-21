from transformers import pipeline, AutoModel, AutoTokenizer, BertTokenizer
from Levenshtein import distance


class Filler_FromWeb:
    MASK_STR = "[MASK]"
    FILL_STR = "exexerrorexex"

    def __init__(self) -> None:
        self.unmasker = pipeline(
            'fill-mask', model='dbmdz/bert-base-italian-xxl-cased', top_k=20)

    def guess(self, sentence: str, masked_word: str) -> str:
        # This is done in order to allow to tokenize/detokenize without
        # problem from brackets
        sentence = sentence.replace(self.FILL_STR, self.MASK_STR)
        results = self.unmasker(sentence)

        # Selecting the closer option among the results
        results = sorted(results, key=lambda x: distance(
            x["token_str"], masked_word))

        return results[0]["token_str"]


class Filler:
    MASK_STR = "[MASK]"
    FILL_STR = "exexerrorexex"
    MODEL_PATH = 'fine_tuning/fine_tuned/'

    def __init__(self) -> None:
        self.unmasker = pipeline(
            'fill-mask', model=self.MODEL_PATH, top_k=20)

    def guess(self, sentence: str, masked_word: str) -> str:
        # This is done in order to allow to tokenize/detokenize without
        # problem from brackets
        sentence = sentence.replace(self.FILL_STR, self.MASK_STR)
        results = self.unmasker(sentence)

        # Selecting the closer option among the results
        results = sorted(results, key=lambda x: distance(
            x["token_str"], masked_word))

        return results[0]["token_str"]


""" a = {'sequence': 'La famiglia era senza un tetto.',
     'score': 0.14316825568675995, 'token': 1335, 'token_str': 'famiglia'} """

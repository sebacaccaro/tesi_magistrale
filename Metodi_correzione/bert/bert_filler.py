from transformers import pipeline, AutoModel, AutoTokenizer, BertTokenizer
from Levenshtein import distance


class Filler:
    MASK_STR = "[MASK]"
    FILL_STR = "exexerrorexex"

    def __init__(self, top_k=20) -> None:
        self.unmasker = pipeline('fill-mask',
                                 model='dbmdz/bert-base-italian-xxl-cased',
                                 top_k=top_k)

    def get_results_unsorted(self, sentence: str) -> list:
        # This is done in order to allow to tokenize/detokenize without
        # problem from brackets
        sentence = sentence.replace(self.FILL_STR, self.MASK_STR)
        results = self.unmasker(sentence)
        return results

    def get_results(self, sentence: str, masked_word: str) -> list:
        results = self.get_results_unsorted(sentence)
        results = sorted(results,
                         key=lambda x: distance(x["token_str"], masked_word))
        return results

    def guess(self, sentence: str, masked_word: str) -> str:
        return self.get_results(sentence, masked_word)[0]["token_str"]


class Filler_from_disk:
    MASK_STR = "[MASK]"
    FILL_STR = "exexerrorexex"
    MODEL_PATH = 'fine_tuning/fine_tuned/'

    def __init__(self) -> None:
        self.unmasker = pipeline('fill-mask', model=self.MODEL_PATH, top_k=20)

    def guess(self, sentence: str, masked_word: str) -> str:
        # This is done in order to allow to tokenize/detokenize without
        # problem from brackets
        sentence = sentence.replace(self.FILL_STR, self.MASK_STR)
        results = self.unmasker(sentence)

        # Selecting the closer option among the results
        results = sorted(results,
                         key=lambda x: distance(x["token_str"], masked_word))

        return results[0]["token_str"]


""" a = {'sequence': 'La famiglia era senza un tetto.',
     'score': 0.14316825568675995, 'token': 1335, 'token_str': 'famiglia'} """

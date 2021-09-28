from logging import error
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch


class Correction_Classifier:
    MODEL_NAME = "fine_tuning/correction_classifier/classifier"

    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained(self.MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(
            self.MODEL_NAME)

    def get_correction_probability(self, error_sentece: str,
                                   correction_sentence: str):
        """ 
        Computes the probability of a correction being correct
        """
        inputs = self.tokenizer(error_sentece,
                                correction_sentence,
                                return_tensors='pt')
        logits = self.model(**inputs)[0]
        results = torch.softmax(logits, dim=1).tolist()[0]
        return results[1]
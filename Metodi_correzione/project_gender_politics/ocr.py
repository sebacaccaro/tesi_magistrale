__project__ = 'gender_politics'
__institution__ = 'University of Milan'
__date__ = 'January 2021'
__comment__ = 'Post OCR Text-correction combining FastText, Word2vec and Normalized Levenshtein Distance.'

#####
# before run:
#  pip3 install gensim
#  pip3 install strsim
#####

from similarity.normalized_levenshtein import NormalizedLevenshtein
from gensim.models import Word2Vec
from gensim.models.fasttext import FastText
from collections import defaultdict
from tqdm import tqdm
from typing import *


class PostOCRTextCorrection:
    '''
    This class helps to correct spelling errors introduced in texts by OCR.
    To correct errors it combines FastText, Word2vec and Normalized Levenshtein Distance .
   '''

    def __init__(self, word2vec:Word2Vec, fasttext:FastText, lexicon:set) -> None:
        '''Creates a new PostOCRTextCorrection object
        Args:
            word2vec (Word2Vec): Word2Vec pre-trained model: a gensim model trained on dirty data (text without cleaning)
            fasttext (FastText): FastText pre-trained model: a gensim model trained on dirty data (text without cleaning)
            lexicon (set): complete list of words belonging to the language of the corpus documents (including conjugations, ...)
        '''

        self.__n_levenshtein = NormalizedLevenshtein()

        # loads pretrained models
        self.word2vec = word2vec
        self.word2vec_vocab = set([word for word in self.word2vec.wv.index_to_key if len(word) > 3])
        self.fasttext = fasttext

        self.lexicon = set(lexicon)

    def __word_in_word2vec__(self, word:str) -> bool:
        '''Returns True if there is a 'word'-vector in Word2vec Space, otherwise False'''
        return word in self.word2vec_vocab

    def __word_in_lexicon__(self, word:str) -> bool:
        '''Returns True if 'word' belongs to the language of the corpus documents'''
        return word in self.lexicon

    def normalized_levhenstein_similarity(self, word1:str, word2:str) -> float:
        '''Returns the normalized levhenstein similarity [0,1] between 'word1' and 'word2' '''
        return self.__n_levenshtein.similarity(word1, word2)

    def weighted_normalized_levhenstein_similarity(self, word1:str, word2:str, weight:float) -> float:
        '''Returns the normalized levhenstein similarity [0,1] between 'word1' and 'word2' weighted
        by 'weight' '''

        return weight * self.normalized_levhenstein_similarity(word1, word2)

    def ocr_correction(self, word:str, topn_we:int=10, topn_nwe=150,
                       weight_we=0.3, weight_nwe=1.0, topn_co:int=1) -> list:
        '''Retrieves the most suitable words to correct the wrong one in input
        Args:
            word (str): a wrong word to correct
            topn_we (int, default=10): top N most similar words if 'word is models embedded
            topn_nwe (int, default=150): top N most similar words if 'word' is not models embedded
            weight_we (float, default=0.3): normalized levhenstein weight if 'word' is models embedded
            weight_nwe (float, default=1.0): normalized levhenstein weight if 'word' is not models embedded
            topn_co (int, default=1): ton N most suitable words to correct the wrong one in input
        Returns:
            list: ton N most suitable words to correct the wrong one in input
        Examples:
          >>> ocr = PostOCRTextCorrection(...)
          >>> word = 'niziitlniente'
          >>> ocr.ocr_correction(word, topn_co=1)
          >>> [('nullatenente', 0.99)] #output
        '''

        word = word.lower()

        # {corrected word: score}
        is_word2vec_embedded = self.__word_in_word2vec__(word)
        corrections_score = defaultdict(int)

        if is_word2vec_embedded:
            for similar_word, cosine_simalirity in self.word2vec.wv.most_similar(word, topn=topn_we):
                if not self.__word_in_lexicon__(similar_word): continue
                corrections_score[similar_word] = \
                    cosine_simalirity + self.weighted_normalized_levhenstein_similarity(word, similar_word, weight_we)
        else:
            # if not self.is_word2vec_embedded(word)
            # we check on a larger neighborod in FastText
            topn_we = topn_nwe

        for similar_word, cosine_simalirity in self.fasttext.wv.most_similar(word, topn=topn_we):
            if not self.__word_in_word2vec__(similar_word): continue

            candidate = list()
            candidate.append(similar_word)

            if is_word2vec_embedded:
                candidate.extend(list(dict(self.word2vec.wv.most_similar(similar_word, topn=topn_we))))
            else:
                pass

            for similar_word in candidate:
                if not self.__word_in_lexicon__(similar_word): continue

                if is_word2vec_embedded:
                    sim = self.word2vec.wv.similarity(word, similar_word) + \
                          self.weighted_normalized_levhenstein_similarity(word, similar_word, weight_we)
                else:
                    sim = cosine_simalirity + \
                          self.weighted_normalized_levhenstein_similarity(word, similar_word, weight_nwe)

                if sim > corrections_score[similar_word]:
                    corrections_score[similar_word] = sim

        return sorted(corrections_score.items(), key=lambda x: x[1], reverse=True)[:topn_co]

    def ocr_correction_corpus(self, data:List[dict], key:str='text', processing_text:callable=lambda x:x,
                              processing_correction:callable=lambda x:x.lower(), min_len:int=5,
                              topn_we: int = 10, topn_nwe=150,
                              weight_we=0.3, weight_nwe=1.0, paragraphs_level:bool = False) -> Tuple[List[dict], dict]:
        '''
        Given a corpus, retrieves ocr errors, estimates corrections for each error, corrects ocr errors with the estimated corrections.
        Args:
            data (List[dict]): a list of json documents
            key (str, default=text): key to the text field in each documents
            processing_text (callable, default=lambda x:x): function to process texts
            processing_correction (callable, default=lambda x:x.lower()): function to process corrections
            min_len (int, default=4): words less than 'min_len' characters long are not corrected.
            topn_we (int, default=10): top N most similar words if 'word' is models embedded
            topn_nwe (int, default=150): top N most similar words if 'word' is not models embedded
            weight_we (float, default=0.3): normalized levhenstein weight if 'word' is models embedded
            weight_nwe (float, default=1.0): normalized levhenstein weight if 'word' is not models embedded
            topn_co (int, default=1): ton N most suitable words to correct the wrong one in input
        Returns:
            Tuple[List[dict], dict]: a list of json documents corrected; corrections
        Examples:
          >>> ocr = PostOCRTextCorrection(...)
          >>> key='text'
          >>> data = [{'text': '[...] niziitlniente [...]'}, ..., {'text': '[...] preliininari [...]'}]
          >>> ocr.ocr_correction(data, key)
          >>> [{'text': '[...] nullatenente [...]'}, ..., {'text': '[...] preliminari [...]'}]#output
        '''
        ocr_errors = set()

        for doc in tqdm(data, position=0, leave=True, desc='Retrieving ocr errors'):
            if paragraphs_level:
                for para_json in doc['paragraphs']:
                    words = set(word for word in processing_text(para_json[key]).split()
                                if len(word) >= min_len and not word.isdigit() and not word[0].isupper())
                    ocr_errors.update(words.difference(self.lexicon))
            else:
                words = set(word for word in processing_text(doc[key]).split()
                            if len(word) >= min_len and not word.isdigit() and not word[0].isupper())
                ocr_errors.update(words.difference(self.lexicon))

        ocr_corrections = dict()
        for ocr_error in tqdm(list(ocr_errors), position=0, leave=True, desc='Retrieving ocr corrections'):
            ocr_correction = self.ocr_correction(ocr_error, topn_we=topn_we, topn_nwe=topn_nwe,
                       weight_we=weight_we, weight_nwe=weight_nwe, topn_co=1)

            if len(ocr_correction) == 0: continue

            ocr_correction = [processing_correction(ocr_corr[0]) for ocr_corr in ocr_correction]
            ocr_corrections[ocr_error] = ocr_correction[0]


        new_data = list()
        for doc in tqdm(data, position=0, leave=True, desc='Correcting ocr errors'):
            if '_id' in doc:
                del doc["_id"]
            if paragraphs_level:
                new_para_json = list()
                for para_json in doc['paragraphs']:
                    para_json[key] = " "+processing_text(para_json[key])+" "
                    for token in para_json[key].split():
                        if token.lower() in ocr_corrections:
                            para_json[key] = para_json[key].replace(" "+token.lower()+" ", " "+ocr_corrections[token.lower()]+" ")
                    new_para_json.append(para_json)
                doc['paragraphs'] = new_para_json
            else:
                doc[key] = " "+processing_text(doc[key])+" "
                for token in doc[key].split():
                    if token.lower() in ocr_corrections:
                        doc[key] = doc[key].replace(" "+token.lower()+" ", " "+ocr_corrections[token.lower()]+" ")
            new_data.append(doc)

        return new_data, ocr_corrections

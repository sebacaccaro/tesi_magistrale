#!/usr/bin/env python3
from bert_filler import Filler
from corrector import Corrector

filler = Filler()
corrector = Corrector("lexicon.txt", filler)


res = corrector.correct("La cssa era seiiza un tetto.")
print(res)

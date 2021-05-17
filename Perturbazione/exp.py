from pipeline import Pipeline, PerturbationModule, TokenizerModule, DetokenizerModule, SplitModuleGenerator, CharsSubModule, AddPunctuationModule, MergeWordHyphenModule, SplitWithCommaModule


# TODO possibile non segmentare l'intera parola, ma dividerla in pezzettoni
# e segmentarne solo alcuni
def split(token):
    return " ".join([char for char in token])


def split_tokens(list_of_tokens):
    return [split(t) for t in list_of_tokens]


subMatrix = {
    "n": {"sub": "ii", "prob": 0.5},
    "rn": {"sub": "m", "prob": 0.5}
}


pipeline = Pipeline()
hypenModule = MergeWordHyphenModule(0.1)
splitModule = SplitModuleGenerator(0.05)
charSub = CharsSubModule(subMatrix)
punctModule = AddPunctuationModule(0.01, ".")
commaModule = SplitWithCommaModule(0.1, ",")


pipeline.addModule(TokenizerModule())

pipeline.addModule(hypenModule)
pipeline.addModule(splitModule)
pipeline.addModule(charSub)
pipeline.addModule(punctModule)
pipeline.addModule(commaModule)

pipeline.addModule(DetokenizerModule())
print(pipeline.run("L’Inter non ha la pancia piena. I nerazzurri superano anche la Roma e trovano la seconda vittoria dopo l’aritmetica dello scudetto: 3-1 a San Siro. Nel primo tempo reti di Brozovic, Vecino e Mkhitaryan. Poco dopo la mezz’ora Sanchez lascia il campo per un problema alla caviglia, entra Lautaro che viene poi sostituito al 77’: battibecco con Conte al momento del cambio. Piccola crepa di un’altra ottima serata per l’Inter, che nella prima metà di secondo tempo deve soffrire per portare a casa i tre punti: l’occasione più importante per la Roma è il palo di Dzeko, nel finale Lukaku chiude la partita in contropiede. Fonseca resta a +2 dal Sassuolo."))

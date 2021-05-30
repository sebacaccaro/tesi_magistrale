from pipelines_def import token_pipeline, segmentation_pipeline, fullPipeline
from pipeline import Pipeline, SuperPipeline, TokenizerModule, DetokenizerModule

subMatrix = {
    "n": {"sub": "ii", "prob": 0.5},
    "rn": {"sub": "m", "prob": 0.5}
}


str1 = "L’Inter non ha la pancia piena. I nerazzurri superano anche la Roma e trovano la seconda vittoria dopo l’aritmetica dello scudetto: 3-1 a San Siro. Nel primo tempo reti di Brozovic, Vecino e Mkhitaryan. Poco dopo la mezz’ora Sanchez lascia il campo per un problema alla caviglia, entra Lautaro che viene poi sostituito al 77’: battibecco con Conte al momento del cambio. Piccola crepa di un’altra ottima serata per l’Inter, che nella prima metà di secondo tempo deve soffrire per portare a casa i tre punti: l’occasione più importante per la Roma è il palo di Dzeko, nel finale Lukaku chiude la partita in contropiede. Fonseca resta a +2 dal Sassuolo."
input = [str1]*4


pip = token_pipeline(1, subMatrix)
pip2 = segmentation_pipeline(
    p_mergehyphen=1,
    p_splitcomma=1,
    p_split=1,
    p_punctadd=1
)
pip4 = segmentation_pipeline(
    p_mergehyphen=0,
    p_splitcomma=0,
    p_split=0,
    p_punctadd=0
)
pip2.addTokenization(TokenizerModule())
pip4.addTokenization(TokenizerModule())


superPip = SuperPipeline(stickyness=0, block_size=300,
                         detokenizer=DetokenizerModule())
superPip.addPipeline(pip4, 1)
superPip.addPipeline(pip2, 1)
print(superPip.run(str1))
#pip2.addTokenization(TokenizerModule(), DetokenizerModule())
#pip.addTokenization(TokenizerModule(), DetokenizerModule())

#pip3 = Pipeline()
# pip3.concatPipeline(pip).concatPipeline(pip2).addTokenization(
#   TokenizerModule(), DetokenizerModule())


#output = pip3.run(str1)
# print(output)
# print(len(str1))

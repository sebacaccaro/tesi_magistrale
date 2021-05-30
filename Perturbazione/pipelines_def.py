from pipeline import Pipeline, PerturbationModule, TokenizerModule, DetokenizerModule, SplitModuleGenerator, CharsSubModule, AddPunctuationModule, MergeWordHyphenModule, SplitWithCommaModule, SuperPipeline


############### TOKEN LEVEL PIPELINES ################
# da 0 a n livello di perturbazione crescente

def token_pipeline(p_charsub, charsub_Matrix):
    pipeline = Pipeline()
    # si potrebbe aggiungere un modulo per droppare dei caratteri
    # o integrar le sostituazioni nulle nella matrice
    pipeline.addModule(CharsSubModule(charsub_Matrix, p_charsub))
    return pipeline


############# SEGMENTATION PIPELINE #######################

def segmentation_pipeline(p_mergehyphen, p_splitcomma, p_split, p_punctadd):
    pipeline = Pipeline()
    pipeline.addModule(MergeWordHyphenModule(p_mergehyphen))
    # Potrebbe essere possibile unire questi due moduli
    pipeline.addModule(SplitWithCommaModule(p_splitcomma, ","))
    pipeline.addModule(SplitModuleGenerator(p_split))
    pipeline.addModule(AddPunctuationModule(p_punctadd, "."))
    return pipeline


############# FULL Pipeline ######################################
def fullPipeline(tkn_pipeline, sgm_pipeleine):
    pipeline = Pipeline()
    pipeline.concatPipeline(tkn_pipeline)
    pipeline.concatPipeline(sgm_pipeleine)
    return pipeline

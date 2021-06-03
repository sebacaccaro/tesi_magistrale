from pipeline import Pipeline, PerturbationModule, TokenizerModule, DetokenizerModule, SplitModuleGenerator, CharsSubModule, AddPunctuationModule, MergeWordHyphenModule, SplitWithCommaModule, SuperPipeline


############### TOKEN LEVEL PIPELINES ################
# da 0 a n livello di perturbazione crescente

def token_pipeline(p_charsub, sub_data):
    pipeline = Pipeline()
    pipeline.addModule(CharsSubModule(sub_data, p_charsub))
    return pipeline


############# SEGMENTATION PIPELINE #######################

def segmentation_pipeline(p_mergehyphen, p_splitcomma, p_split, p_punctadd):
    pipeline = Pipeline()
    pipeline.addModule(MergeWordHyphenModule(p_mergehyphen))
    # Potrebbe essere possibile unire questi due moduli
    pipeline.addModule(SplitWithCommaModule(p_splitcomma, ","))
    pipeline.addModule(SplitModuleGenerator(p_split))
    pipeline.addModule(AddPunctuationModule(p_punctadd, "."))
    pipeline.addModule(AddPunctuationModule(p_punctadd/2, ","))
    pipeline.addModule(AddPunctuationModule(p_punctadd/2, "'"))
    return pipeline


############# FULL Pipeline ######################################
def fullPipeline(tkn_pipeline, sgm_pipeleine):
    pipeline = Pipeline()
    pipeline.concatPipeline(tkn_pipeline)
    pipeline.concatPipeline(sgm_pipeleine)
    return pipeline

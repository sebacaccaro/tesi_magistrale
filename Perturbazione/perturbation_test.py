import json
from pipeline import DetokenizerModule, SuperPipeline, TokenizerModule
from pipelines_def import segmentation_pipeline, token_pipeline

with open("XVIII_legislature_italian_republic.json") as f:
    inputText = json.load(f)[22]["text"]

with open("./submatrix_extraction/confusionMatrix.json") as f:
    subData = json.load(f)


easySegPipeline = segmentation_pipeline(
    p_mergehyphen=0.001,
    p_splitcomma=0.001,
    p_split=0.0025,
    p_punctadd=0.005
)

mediumSegPipeline = segmentation_pipeline(
    p_mergehyphen=0.001,
    p_splitcomma=0.002,
    p_split=0.008,
    p_punctadd=0.025
)

hardSegPipeline = segmentation_pipeline(
    p_mergehyphen=0.01,
    p_splitcomma=0.02,
    p_split=0.05,
    p_punctadd=0.1
)

easySegPipeline.addTokenization(TokenizerModule())
mediumSegPipeline.addTokenization(TokenizerModule())
hardSegPipeline.addTokenization(TokenizerModule())


segmentation_error_super_1 = SuperPipeline(
    stickyness=0.8,
    block_size=800,
    detokenizer=DetokenizerModule()
)

segmentation_error_super_2 = SuperPipeline(
    stickyness=0.8,
    block_size=800,
    detokenizer=DetokenizerModule()
)

segmentation_error_super_3 = SuperPipeline(
    stickyness=0.8,
    block_size=800,
    detokenizer=DetokenizerModule()
)


segmentation_error_super_1.addPipeline(easySegPipeline, weight=6)
segmentation_error_super_1.addPipeline(mediumSegPipeline, weight=4)
segmentation_error_super_1.addPipeline(hardSegPipeline, weight=1)

segmentation_error_super_2.addPipeline(easySegPipeline, weight=2)
segmentation_error_super_2.addPipeline(mediumSegPipeline, weight=8)
segmentation_error_super_2.addPipeline(hardSegPipeline, weight=1)

segmentation_error_super_3.addPipeline(easySegPipeline, weight=1)
segmentation_error_super_3.addPipeline(mediumSegPipeline, weight=6)
segmentation_error_super_3.addPipeline(hardSegPipeline, weight=4)

easyTknPipeline = token_pipeline(
    p_charsub=0.1,
    sub_data=subData
)

mediumTknPipeline = token_pipeline(
    p_charsub=0.3,
    sub_data=subData
)

hardTknPipeline = token_pipeline(
    p_charsub=0.8,
    sub_data=subData
)


easyTknPipeline.addTokenization(TokenizerModule())
mediumTknPipeline.addTokenization(TokenizerModule())
hardTknPipeline.addTokenization(TokenizerModule())

tokenization_error_super_1 = SuperPipeline(
    stickyness=0.8,
    block_size=800,
    detokenizer=DetokenizerModule()
)

tokenization_error_super_2 = SuperPipeline(
    stickyness=0.8,
    block_size=800,
    detokenizer=DetokenizerModule()
)

tokenization_error_super_3 = SuperPipeline(
    stickyness=0.8,
    block_size=800,
    detokenizer=DetokenizerModule()
)

tokenization_error_super_1.addPipeline(easyTknPipeline, weight=6)
tokenization_error_super_1.addPipeline(mediumTknPipeline, weight=4)
tokenization_error_super_1.addPipeline(hardTknPipeline, weight=1)

tokenization_error_super_2.addPipeline(easyTknPipeline, weight=2)
tokenization_error_super_2.addPipeline(mediumTknPipeline, weight=8)
tokenization_error_super_2.addPipeline(hardTknPipeline, weight=1)

tokenization_error_super_3.addPipeline(easyTknPipeline, weight=1)
tokenization_error_super_3.addPipeline(mediumTknPipeline, weight=6)
tokenization_error_super_3.addPipeline(hardTknPipeline, weight=4)


output = tokenization_error_super_2.run(inputText)

with open("perturbed_output.md", "w") as f:
    f.write(output)

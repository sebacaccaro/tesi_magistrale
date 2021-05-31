import json
from pipeline import DetokenizerModule, SuperPipeline, TokenizerModule
from pipelines_def import segmentation_pipeline

with open("XVIII_legislature_italian_republic.json") as f:
    inputText = json.load(f)[22]["text"]


easyPipeline = segmentation_pipeline(
    p_mergehyphen=0.001,
    p_splitcomma=0.001,
    p_split=0.0025,
    p_punctadd=0.005
)

mediumPipeline = segmentation_pipeline(
    p_mergehyphen=0.001,
    p_splitcomma=0.002,
    p_split=0.008,
    p_punctadd=0.025
)

hardPipeline = segmentation_pipeline(
    p_mergehyphen=0.01,
    p_splitcomma=0.02,
    p_split=0.05,
    p_punctadd=0.1
)

easyPipeline.addTokenization(TokenizerModule())
mediumPipeline.addTokenization(TokenizerModule())
hardPipeline.addTokenization(TokenizerModule())


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


segmentation_error_super_1.addPipeline(easyPipeline, weight=6)
segmentation_error_super_1.addPipeline(mediumPipeline, weight=4)
segmentation_error_super_1.addPipeline(hardPipeline, weight=1)

segmentation_error_super_2.addPipeline(easyPipeline, weight=2)
segmentation_error_super_2.addPipeline(mediumPipeline, weight=8)
segmentation_error_super_2.addPipeline(hardPipeline, weight=1)

segmentation_error_super_3.addPipeline(easyPipeline, weight=1)
segmentation_error_super_3.addPipeline(mediumPipeline, weight=6)
segmentation_error_super_3.addPipeline(hardPipeline, weight=4)

output = segmentation_error_super_3.run(inputText)

with open("perturbed_output.md", "w") as f:
    f.write(output)

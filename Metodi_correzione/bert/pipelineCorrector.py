class PipelineCorrector:
    def __init__(self) -> None:
        self.correctors = []

    def addCorrector(self, corrector):
        self.correctors.append(corrector)

    def correct(self, sentence: str):
        for corrector in self.correctors:
            sentence = corrector.correct(sentence)
        return sentence

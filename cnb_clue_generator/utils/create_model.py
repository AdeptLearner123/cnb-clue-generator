from cnb_clue_generator.clue_generator.gpt_fine_tuned_clue_generator import GPTFineTunedClueGenerator
from cnb_clue_generator.clue_generator.gpt_piecewise_clue_generator import GPTPiecewiseClueGenerator
from cnb_clue_generator.clue_generator.vector_clue_generator import Word2VecGlueGenerator, GloveNetClueGenerator
from cnb_clue_generator.clue_generator.gpt_simple_clue_generator import GPTSimpleClueGenerator


def create_model(model_name):
    if model_name == "gpt":
        return GPTFineTunedClueGenerator()
    elif model_name == "piecewise-gpt":
        return GPTPiecewiseClueGenerator()
    elif model_name == "simple-gpt":
        return GPTSimpleClueGenerator()
    elif model_name == "word2vec":
        return Word2VecGlueGenerator()
    elif model_name == "glovenet":
        return GloveNetClueGenerator()
    raise ValueError("Invalid model name")

from .clue_generator_base import ClueGeneratorBase
from cnb_clue_generator.utils.gpt_completion_model import GPTCompletionModel

from config import SIMPLE_PROMPT

class GPTSimpleClueGenerator(ClueGeneratorBase, GPTCompletionModel):
    def __init__(self):
        super().__init__()

        with open(SIMPLE_PROMPT, "r") as file:
            self._simple_prompt = file.read()
    
    def generate_clue(self, pos_words, neg_words):
        pos_words_str = ", ".join([ word.lower() for word in pos_words ])
        prompt = self._simple_prompt + "\n\n" + "answers: " + pos_words_str + "\n" + "clue:"
        completion = self._get_completion(prompt)
        clue = completion.strip().upper()
        return clue, pos_words, [""] * len(pos_words)
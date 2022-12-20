from config import FEW_SHOT_PROMPT
from cnb_clue_generator.utils.gpt_completion_model import GPTCompletionModel
from .clue_generator_base import ClueGeneratorBase

import openai

class GPTFewShotClueGenerator(ClueGeneratorBase, GPTCompletionModel):
    FEW_SHOT_PROMPT = "Give a single-word clue that links to as many of the positive words as possible, while avoiding the negative words and list which positive words it is linked with. Explain why each positive word is related."

    def __init__(self):
        super().__init__()

        with open(FEW_SHOT_PROMPT, "r") as file:
            self._few_shot_prompt = file.read()


    def _create_prompt(self, pos_words, neg_words):
        return self._few_shot_prompt + "\n" + \
            f"Positive: {', '.join(pos_words)}\n" + \
            f"Negative: {', '.join(neg_words)}\n" + \
            "Clue:"


    def _parse_completion(self, completion):
        lines = completion.splitlines()
        clue = lines[0].strip()
        clue_words = lines[1].split(":")[1].strip().split(", ")
        explanations = lines[2:]
        return clue, clue_words, explanations
    

    def generate_clue(self, pos_words, neg_words):
        prompt = self._create_prompt(pos_words, neg_words)
        completion = self._get_completion(prompt)
        clue, clue_words, explanations = self._parse_completion(completion.choices[0].text)
        return clue, clue_words, explanations
    

    def print_usage(self):
        print(self.get_usage())
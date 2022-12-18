from config import FEW_SHOT_PROMPT
from .clue_generator_base import ClueGeneratorBase

import openai

class GPTFewShotClueGenerator(ClueGeneratorBase):
    FEW_SHOT_PROMPT = "Give a single-word clue that links to as many of the positive words as possible, while avoiding the negative words and list which positive words it is linked with. Explain why each positive word is related."

    def __init__(self):
        self._prompt_tokens = 0
        self._completion_tokens = 0
        self._total_tokens = 0

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


    def _update_usage(self, usage):
        self._prompt_tokens += usage["prompt_tokens"]
        self._completion_tokens += usage["completion_tokens"]
        self._total_tokens += usage["total_tokens"]


    def get_usage(self):
        return self._prompt_tokens, self._completion_tokens, self._total_tokens
    

    def generate_clue(self, pos_words, neg_words):
        prompt = self._create_prompt(pos_words, neg_words)
        completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, temperature=0, max_tokens=256)
        #print(completion.choices[0].text)
        self._update_usage(completion.usage)

        clue, clue_words, explanations = self._parse_completion(completion.choices[0].text)
        return clue, clue_words, explanations
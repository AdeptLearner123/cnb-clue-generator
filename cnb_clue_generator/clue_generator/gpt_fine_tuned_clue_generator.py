from .clue_generator_base import ClueGeneratorBase

import openai

class GPTFineTunedClueGenerator(ClueGeneratorBase):
    PROMPT_END_TOKEN = "\n\n###\n\n"
    END_TOKEN = " END"

    def __init__(self):
        self._prompt_tokens = 0
        self._completion_tokens = 0
        self._total_tokens = 0


    def _create_prompt(self, pos_words, neg_words):
        return \
            "positive: " + ", ".join(pos_words) + "\n" + \
            "negative: " + ", ".join(neg_words) + self.PROMPT_END_TOKEN


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
        print("Prompt")
        print(prompt)
        completion = openai.Completion.create(model="davinci:ft-personal:board-clue-generator-2022-12-16-00-51-01", prompt=prompt, temperature=0, max_tokens=512, stop=" END")
        print("Completed")
        print(completion.choices[0].text)
        self._update_usage(completion.usage)

        clue, clue_words, explanations = self._parse_completion(completion.choices[0].text)
        return clue, clue_words, explanations
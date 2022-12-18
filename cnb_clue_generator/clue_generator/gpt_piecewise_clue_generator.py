from .gpt_clue_generator_base import GPTClueGeneratorBase

import itertools

class GPTPiecewiseClueGenerator(GPTClueGeneratorBase):
    def generate_clue(self, pos_words, neg_words):
        return super().generate_clue(pos_words, neg_words)
    




    def _get_relatedness(self, word1, word2):
        prompt = f"Determine whether {word1} and {word2} are related or unrelated in one word"
        completion = self._get_completion(prompt)
        answer = completion.strip().strip(".")
        return answer.lower() == "related"


    def _propose_clue(self, pos_words, neg_words):
        pos_words_str = ", ".join(pos_words)
        neg_words_str = ", ".join(neg_words)

        if len(neg_words) > 0:
            prompt = f"Give a single-word Code Names clues that links {pos_words_str} but not {neg_words_str}:"
        else:
            prompt = f"Give a single-word Code Names clues that links {pos_words_str}:"
        
        completion = self._get_completion(prompt)
        clue = completion.strip().strip(".").upper()
        return clue
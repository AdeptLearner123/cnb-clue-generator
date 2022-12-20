from cnb_clue_generator.utils.gpt_completion_model import GPTCompletionModel

class GPTRelationClassifier(GPTCompletionModel):
    def __init__(self):
        self._cache = dict()
        super().__init__()

    def get_relatedness(self, word1, word2):
        key = frozenset([ word1, word2 ])
        if key in self._cache:
            return self._cache[key]

        prompt = f"Determine whether {word1} and {word2} are related or unrelated in one word"
        completion = self._get_completion(prompt)
        answer = completion.strip().strip(".")
        is_related = answer.lower() == "related"
        self._cache[key] = is_related
        return is_related
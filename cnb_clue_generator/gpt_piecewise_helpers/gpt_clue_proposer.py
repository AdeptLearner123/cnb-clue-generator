from cnb_clue_generator.utils.gpt_completion_model import GPTCompletionModel

class GPTClueProposer(GPTCompletionModel):
    def __init__(self):
        self._cache = dict()
        super().__init__()


    def propose_clue(self, pos_words, neg_words):
        key = (frozenset(pos_words), frozenset(neg_words))
        if key in self._cache:
            return self._cache[key]

        pos_words_str = ", ".join(pos_words)
        neg_words_str = ", ".join(neg_words)

        if len(neg_words) > 0:
            prompt = f"Give a single-word Code Names clues that distinguishes {pos_words_str} from {neg_words_str}:"
        else:
            prompt = f"Give a single-word Code Names clues that links {pos_words_str}:"
        
        completion = self._get_completion(prompt)
        clue = completion.strip().strip(".").upper()

        self._cache[key] = clue
        return clue
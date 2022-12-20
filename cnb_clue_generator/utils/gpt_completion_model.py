import openai

class GPTCompletionModel:

    def __init__(self):
        self._prompt_tokens = 0
        self._completion_tokens = 0
        self._total_tokens = 0
        self._completions = 0


    def _update_usage(self, usage):
        self._prompt_tokens += usage["prompt_tokens"]
        self._completion_tokens += usage["completion_tokens"]
        self._total_tokens += usage["total_tokens"]
        self._completions += 1


    def get_usage(self):
        return {
            "completions": self._completions,
            "prompt tokens": self._prompt_tokens, 
            "completion tokens": self._completion_tokens,
            "total tokens": self._total_tokens
        }


    def _get_completion(self, prompt):
        completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, temperature=0, top_p=0, max_tokens=256)
        self._update_usage(completion.usage)
        return completion.choices[0].text
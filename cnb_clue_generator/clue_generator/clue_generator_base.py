from abc import ABC, abstractmethod

class ClueGeneratorBase(ABC):
    @abstractmethod
    def generate_clue(self, pos_words, neg_words):
        pass
    

    def print_usage(self):
        print("No usage")
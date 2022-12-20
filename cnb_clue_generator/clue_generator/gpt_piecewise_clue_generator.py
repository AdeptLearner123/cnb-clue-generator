from .clue_generator_base import ClueGeneratorBase
from cnb_clue_generator.gpt_piecewise_helpers.gpt_clue_proposer import GPTClueProposer
from cnb_clue_generator.gpt_piecewise_helpers.gpt_relation_classifier import GPTRelationClassifier

from itertools import combinations
from collections import defaultdict

class GPTPiecewiseClueGenerator(ClueGeneratorBase):
    def __init__(self):
        self._clue_proposer = GPTClueProposer()
        self._relation_classifier = GPTRelationClassifier()


    def generate_clue(self, pos_words, neg_words):
        clue_words = dict()
        combo_clues = self._get_clues_ignore_negs(pos_words)
        print("Combo clues", combo_clues)
        self._update_clue_words(combo_clues.items(), clue_words, neg_words)
        combo_clues_with_neg = self._get_clues_with_negs(combo_clues, clue_words)
        self._update_clue_words(combo_clues_with_neg, clue_words, neg_words)
        return self._get_best_clue(clue_words)


    def print_usage(self):
        print("Clue proposer usage")
        print(self._clue_proposer.get_usage())
        print("Relation classifier usage")
        print(self._relation_classifier.get_usage())


    def _get_best_clue(self, clue_words):
        print("Clue words", clue_words)
        valid_clues = [ clue for clue in clue_words if len(clue_words[clue][1]) == 0 ]
        best_clue = max(valid_clues, key=lambda clue: len(clue_words[clue][0]))
        clue_words = list(clue_words[best_clue][0])
        return best_clue, clue_words, [""] * len(clue_words)


    def _get_clue_pos_neg_counts(self, word_clues, pos_words, neg_words):
        pos_counts = defaultdict(lambda: 0)
        neg_counts = defaultdict(lambda: 0)
        
        for word in pos_words:
            for clue in word_clues[word]:
                pos_counts[clue] += 1
        
        for word in neg_words:
            for clue in word_clues[word]:
                neg_counts[clue] += 1
        
        all_clues = set(pos_words.keys()).union(set(neg_words.keys()))
        return { clue: (pos_counts[clue], neg_counts[clue]) for clue in all_clues }


    def _get_clues_with_negs(self, combo_clues, clue_words):
        combo_clues_with_neg = []

        for combo, clue in combo_clues.items():
            _, clue_neg_words = clue_words[clue]
            if len(clue_neg_words) > 0:
                clue_with_neg = self._propose_clue(list(combo), clue_neg_words)
                if clue_with_neg is not None:
                    combo_clues_with_neg.append((combo, clue_with_neg))
        return combo_clues_with_neg


    def _update_clue_words(self, clues, clue_words, neg_words):
        for pos_words, clue in clues:
            clue_neg_words = set()
            for word in neg_words:
                if self._relation_classifier.get_relatedness(word, clue):
                    clue_neg_words.add(word)
            clue_words[clue] = (set(pos_words), clue_neg_words)
        return clue_words


    def _get_clues_ignore_negs(self, pos_words):
        combo_clues = dict()

        for i in range(1, 1 + len(pos_words)):
            for combo in combinations(pos_words, i):
                self._get_combo_clue(combo_clues, combo)
        
        return combo_clues
            

    def _get_combo_clue(self, combo_clues, pos_words):
        if len(pos_words) > 1:
            for sub_combo in combinations(pos_words, len(pos_words) - 1):
                if frozenset(sub_combo) not in combo_clues:
                    return

        clue = self._propose_clue(pos_words)
        print("Combo", pos_words, clue)
        
        if clue is not None:
            combo_clues[frozenset(pos_words)] = clue
    

    def _propose_clue(self, pos_words, neg_words = []):
        clue = self._clue_proposer.propose_clue(pos_words, neg_words)
        for pos_word in pos_words:
            if not self._relation_classifier.get_relatedness(pos_word, clue):
                return None
        return clue
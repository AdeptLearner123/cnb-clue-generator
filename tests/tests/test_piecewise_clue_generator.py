from cnb_clue_generator.clue_generator.gpt_piecewise_clue_generator import GPTPiecewiseClueGenerator

import os
import json
from unittest.mock import Mock

TEST_SCENARIOS = "tests/data/piecewise_scenarios"

def test_piecewise():
    for filename in os.listdir(TEST_SCENARIOS):
        with open(os.path.join(TEST_SCENARIOS, filename)) as file:
            base_test_piecewise_scenario(json.loads(file.read()))


def base_test_piecewise_scenario(scenario):
    clue_generator = GPTPiecewiseClueGenerator()

    propsoal_to_clue = { (tuple(sorted(proposal["pos"])), tuple(sorted(proposal["neg"]))): proposal["clue"] for proposal in scenario["proposals"] }
    def mock_propose_clue(pos_words, neg_words):
        pos_words = tuple(sorted(pos_words))
        neg_words = tuple(sorted(neg_words))
        key = (pos_words, neg_words)
        if key in propsoal_to_clue:
            return propsoal_to_clue[key]
        return "Random clue"
    
    relations = set([ tuple(word_pair) for word_pair in scenario["relations"] ])
    def mock_relation_classifier(word1, word2):
        return tuple([word1, word2]) in relations

    clue_generator._clue_proposer.propose_clue = Mock(side_effect=mock_propose_clue)
    clue_generator._relation_classifier.get_relatedness = Mock(side_effect = mock_relation_classifier)
    clue, clue_words, _ = clue_generator.generate_clue(scenario["pos"], scenario["neg"])
    assert clue == scenario["clue"]
    assert set(clue_words) == set(scenario["clue_words"])
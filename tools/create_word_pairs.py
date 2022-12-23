from config import WORD_PAIRS, CARDWORDS

import json
import random

def main():
    with open(CARDWORDS, "r") as file:
        words = file.read().splitlines()
    
    with open(WORD_PAIRS, "r") as file:
        word_pairs = json.loads(file.read())

    while True:
        sample = random.sample(words, 4)
        print("Words:", sample)
        word1 = input("word 1:")
        word2 = input("word 2:")

        if word1 not in sample or word2 not in sample:
            print("Invalid words")
            continue
        
        clue = input("clue:")
        explanation_1 = input("explanation 1:")
        explanation_2 = input("explanation 2:")

        word_pairs.append({
            "word1": word1,
            "word2": word2,
            "clue": clue,
            "explanation1": explanation_1,
            "explanation2": explanation_2
        })

        with open(WORD_PAIRS, "w+") as file:
            file.write(json.dumps(word_pairs, indent=4))


if __name__ == "__main__":
    main()
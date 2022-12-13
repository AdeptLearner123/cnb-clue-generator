from config import CARDWORDS, BOARDS

import json
import random
import uuid

POSITIVE_WORDS = 9
BLANK_WORDS = 8
ENEMY_WORDS = 8

NUM_BOARDS = 50

def main():
    with open(CARDWORDS, "r") as file:
        cardwords = file.read().splitlines()

    boards = dict()

    for _ in range(NUM_BOARDS):
        id = str(uuid.uuid4())
        boards[id] = create_board(cardwords)

    with open(BOARDS, "w+") as file:
        file.write(json.dumps(boards, indent=4))


def create_board(cardwords):
    num_pos = random.randint(1, POSITIVE_WORDS)
    num_neg = random.randint(BLANK_WORDS, BLANK_WORDS + ENEMY_WORDS)
    words = random.sample(cardwords, num_pos + num_neg)
    pos_words = words[:num_pos]
    neg_words = words[num_pos:]

    return {
        "pos": pos_words,
        "neg": neg_words
    }


if __name__ == "__main__":
    main()
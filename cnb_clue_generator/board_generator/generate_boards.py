from config import CARDWORDS, BOARDS

import json
import random
import uuid
from argparse import ArgumentParser
import os

POSITIVE_WORDS = 9
BLANK_WORDS = 8
ENEMY_WORDS = 8

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-n", "--number", type=int, required=True)
    parser.add_argument("-f", "--file-name", type=str, required=True)
    parser.add_argument("--min-pos", type=int, required=False, default=1)
    parser.add_argument("--max-pos", type=int, required=False, default=POSITIVE_WORDS)
    parser.add_argument("--min-neg", type=int, required=False, default=BLANK_WORDS)
    parser.add_argument("--max-neg", type=int, required=False, default=BLANK_WORDS + ENEMY_WORDS)
    args = parser.parse_args()
    return args.number, args.file_name, args.min_pos, args.max_pos, args.min_neg, args.max_neg


def get_boards(file_path):
    if not os.path.exists(BOARDS):
        os.mkdir(BOARDS)
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            boards = json.loads(file.read())
    else:
        boards = dict()
    return boards


def main():
    number, file_name, min_pos, max_pos, min_neg, max_neg = parse_args()

    with open(CARDWORDS, "r") as file:
        cardwords = file.read().splitlines()

    file_path = os.path.join(BOARDS, f"{file_name}.json")
    boards = get_boards(file_path)

    for _ in range(number):
        id = str(uuid.uuid4())
        boards[id] = create_board(cardwords, min_pos, max_pos, min_neg, max_neg)

    with open(file_path, "w+") as file:
        file.write(json.dumps(boards, indent=4))


def create_board(cardwords, min_pos, max_pos, min_neg, max_neg):
    num_pos = random.randint(min_pos, max_pos)
    num_neg = random.randint(min_neg, max_neg)
    words = random.sample(cardwords, num_pos + num_neg)
    pos_words = words[:num_pos]
    neg_words = words[num_pos:]

    return {
        "pos": pos_words,
        "neg": neg_words
    }


if __name__ == "__main__":
    main()
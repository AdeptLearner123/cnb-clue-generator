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
    args = parser.parse_args()
    return args.number, args.file_name


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
    number, file_name = parse_args()

    with open(CARDWORDS, "r") as file:
        cardwords = file.read().splitlines()

    file_path = os.path.join(BOARDS, f"{file_name}.json")
    boards = get_boards(file_path)

    for _ in range(number):
        id = str(uuid.uuid4())
        boards[id] = create_board(cardwords)

    with open(file_path, "w+") as file:
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
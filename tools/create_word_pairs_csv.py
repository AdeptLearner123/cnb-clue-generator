from config import CARDWORDS, WORD_PAIRS_CSV

import random
from argparse import ArgumentParser
import os

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-n", type=int, required=True)
    parser.add_argument("-f", type=str, required=True)
    args = parser.parse_args()
    return args.n, args.f


def main():
    if not os.path.exists(WORD_PAIRS_CSV):
        os.mkdir(WORD_PAIRS_CSV)

    num, file = parse_args()
    file_path = os.path.join(WORD_PAIRS_CSV, f"{file}.csv")

    with open(CARDWORDS, "r") as file:
        words = file.read().splitlines()
    
    lines = [ "Word 1, Word 2" ]
    for _ in range(num):
        pair = random.sample(words, 2)
        lines.append(", ".join(pair))
    
    with open(file_path, "w+") as file:
        file.write("\n".join(lines))


if __name__ == "__main__":
    main()
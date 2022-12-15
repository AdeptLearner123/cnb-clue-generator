from config import GENERATED_CLUES, BOARDS

from argparse import ArgumentParser
import json
import os
import random

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file-name", type=str, required=True)
    args = parser.parse_args()
    return args.file_name


def prompt_guess(words):
    while True:
        guess = input("Guess:")
        if len(guess) == 0:
            return None
        if guess not in words:
            print("Invalid guess")
            continue
        return guess


def prompt_guesses(board, clue):
    words = board["pos"] + board["neg"]
    random.shuffle(words)
    print("Words:", ", ".join(words))
    print("Clue:", clue)

    guesses = []
    while True:
        guess = prompt_guess(words)
        if guess is None:
            break
        guesses.append(guess)
    
    return guesses


def get_guesses(board_id, boards, clue, num):
    board = boards[board_id]

    if "guesses" not in board:
        board["guesses"] = dict()
    
    if clue not in board["guesses"]:
        board["guesses"][clue] = prompt_guesses(board, clue, num)

        with open(BOARDS, "w") as file:
            file.write(json.dumps(boards, indent=4))
    
    return board["guesses"][clue]


def main():
    file_name = parse_args()
    file_path = os.path.join(GENERATED_CLUES, f"{file_name}.json")

    with open(file_path, "r") as file:
        board_clues = json.loads(file.read())        

    with open(BOARDS, "r") as file:
        boards = json.loads(file.read())

    total_correct, total_incorrect = 0, 0
    unrelated_positives = []
    guessed_negatives = []

    for board_id, board_clue in board_clues.items():
        clue = board_clue["clue"]
        clue_words = board_clue["clue_words"]

        all_clue_guesses = get_guesses(board_id, boards, clue)
        clue_guesses = all_clue_guesses[:len(clue_words)]
        
        correct = len(set(clue_words).intersection(set(clue_guesses)))
        incorrect = len(clue_words) - correct
        total_correct += correct
        total_incorrect += incorrect

        unrelated_positives += [ (clue, word) for word in clue_words if word not in all_clue_guesses]
        guessed_negatives += [ (clue, word) for word in clue_guesses if word not in clue_words]
    
    print("Correct", total_correct)
    print("Incorrect", total_incorrect)
    print("Score", (total_correct - total_incorrect) / len(boards))
    print("Unrelatd Positives", len(unrelated_positives))
    print("Guessed Negatives", len(guessed_negatives))

    for clue, word in unrelated_positives:
        print()
        print("Unrelated Positives:")
        print("\t", clue, "  ", word)

    for clue, word in guessed_negatives:
        print()
        print("Guessed Negatives:")
        print("\t", clue, "  ", word)

if __name__ == "__main__":
    main()
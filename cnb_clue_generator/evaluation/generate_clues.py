from config import BOARDS, GENERATED_CLUES
from cnb_clue_generator.clue_generator.gpt_clue_generator import GPTClueGenerator

from argparse import ArgumentParser
import json
import os
from tqdm import tqdm

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file-name", type=str, required=True)
    parser.add_argument("-k", "--api-key", type=str, required=True)
    args = parser.parse_args()
    return args.file_name, args.api_key


def read_generated_clues(file_path):
    if not os.path.exists(GENERATED_CLUES):
        os.path.mkdir(GENERATED_CLUES)

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.loads(file.read())
    else:
        return dict()


def main():
    file_name, api_key = parse_args()
    clue_generator = GPTClueGenerator(api_key)
    
    with open(BOARDS, "r") as file:
        boards = json.loads(file.read())
    
    file_path = os.path.join(GENERATED_CLUES, f"{file_name}.json")
    generated_clues = read_generated_clues(file_name)
    unclued_boards = set(boards.keys()) - set(generated_clues.keys())

    print("Scenarios:", len(boards), "Missing:", len(unclued_boards))

    for board_id in tqdm(list(unclued_boards)):
        board = boards[board_id]
        pos_words = board["pos"]
        neg_words = board["neg"]

        clue, clue_words, explanations = clue_generator.generate_clue(pos_words, neg_words)
        
        generated_clues[board_id] = {
            "clue": clue,
            "clue_words": clue_words,
            "explanations": explanations
        }

        with open(file_path, "w+") as file:
            file.write(json.dumps(generated_clues, indent=4))
    
        print("Usage:", clue_generator.get_usage())


if __name__ == "__main__":
    main()
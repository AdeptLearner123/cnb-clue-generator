from config import BOARDS, GENERATED_CLUES
from cnb_clue_generator.utils.create_model import create_model

from argparse import ArgumentParser
import json
import os
import openai
from tqdm import tqdm

openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-m", "--model-name", type=str, required=True)
    parser.add_argument("-f", "--file-name", type=str, required=True)
    parser.add_argument("-b", "--boards-file", type=str, required=True)
    args = parser.parse_args()
    return args.file_name, args.boards_file, args.model_name


def read_generated_clues(file_path):
    if not os.path.exists(GENERATED_CLUES):
        os.path.mkdir(GENERATED_CLUES)

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.loads(file.read())
    else:
        return dict()


def main():
    file_name, boards_file, model_name = parse_args()
    clue_generator = create_model(model_name)
    
    with open(os.path.join(BOARDS, f"{boards_file}.json"), "r") as file:
        boards = json.loads(file.read())
    
    file_path = os.path.join(GENERATED_CLUES, f"{file_name}.json")
    generated_clues = read_generated_clues(file_path)
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
    
        #print("Usage:", clue_generator.get_usage())


if __name__ == "__main__":
    main()
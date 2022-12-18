from config import TRAIN_DATA, TRAIN_BOARDS

import json

def main():
    with open(TRAIN_BOARDS, "r") as file:
        boards = json.loads(file.read())
    
    data = []
    for board in boards.values():
        prompt = \
            "positive: " + ", ".join(board["pos"]) + "\n" + \
            "negative: " + ", ".join(board["neg"]) + \
            "\n\n###\n\n"
        
        completion = \
            "clue: " + board["clue"] + "\n" + \
            "clue words: " + ", ".join(board["clue_words"]) + "\n\n" + \
            "\n".join(list(board["pos_explanations"].values()) + list(board["neg_explanations"].values())) + \
            " END"
        
        data.append({
            "prompt": prompt,
            "completion": completion
        })
        
    with open(TRAIN_DATA, "w+") as file:
        file.write(json.dumps(data, indent=4))


if __name__ == "__main__":
    main()
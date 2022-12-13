from cnb_clue_generator.clue_generator.gpt_clue_generator import GPTClueGenerator

from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-k", "--api-key", type=str, required=True)
    parser.add_argument("-p","--positive", nargs="+", required=True)
    parser.add_argument("-n","--negative", nargs="+", required=True)
    args = parser.parse_args()
    return args.positive, args.negative, args.api_key


def main():
    pos_words, neg_words, api_key = parse_args()

    clue_generator = GPTClueGenerator(api_key)
    clue, clue_words, explanations = clue_generator.generate_clue(pos_words, neg_words)

    print("Clue:", clue)
    print("Clue words:", clue_words)
    print("Explanations:")
    print("\n".join(explanations))

    print()
    print("Usage:", clue_generator.get_usage())


if __name__ == "__main__":
    main()
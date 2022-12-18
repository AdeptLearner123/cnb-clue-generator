from cnb_clue_generator.clue_generator.gpt_fine_tuned_clue_generator import GPTFineTunedClueGenerator

from argparse import ArgumentParser
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-p","--positive", nargs="+", required=True)
    parser.add_argument("-n","--negative", nargs="+", required=True)
    args = parser.parse_args()
    return args.positive, args.negative


def main():
    pos_words, neg_words = parse_args()

    clue_generator = GPTFineTunedClueGenerator()
    clue, clue_words, explanations = clue_generator.generate_clue(pos_words, neg_words)

    print("Clue:", clue)
    print("Clue words:", clue_words)
    print("Explanations:")
    print("\n".join(explanations))

    print()
    print("Usage:", clue_generator.get_usage())


if __name__ == "__main__":
    main()
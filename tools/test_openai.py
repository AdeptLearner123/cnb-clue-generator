import openai

from argparse import ArgumentParser
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-p", "--prompt", type=str)
    args = parser.parse_args()
    return args.prompt


def main():
    prompt = parse_args()
    completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, temperature=0, max_tokens=256)
    print(completion.choices[0].text)


if __name__ == "__main__":
    main()
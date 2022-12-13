import openai

from argparse import ArgumentParser

def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-p", "--prompt", type=str)
    parser.add_argument("-k", "--api-key", type=str, required=True)
    args = parser.parse_args()
    return args.prompt, args.api_key


def main():
    prompt, api_key = parse_args()

    openai.api_key = api_key

    completion = openai.Completion.create(engine="text-davinci-003", prompt=prompt, temperature=0, max_tokens=256)
    print(completion.choices[0].text)


if __name__ == "__main__":
    main()
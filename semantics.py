import json
import pathlib
import re

import click
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.wsd import lesk
from tqdm import tqdm


def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [
        token for token in tokens if token.isalnum() and token not in stop_words
    ]

    return filtered_tokens


def sim(phrase1, phrase2):
    tokens1 = preprocess_text(phrase1)
    tokens2 = preprocess_text(phrase2)

    synsets1 = [lesk(tokens1, token) for token in tokens1]
    synsets2 = [lesk(tokens2, token) for token in tokens2]

    similarity_score = 0
    count = 0

    for synset1 in synsets1:
        if synset1 is None:
            continue

        for synset2 in synsets2:
            if synset2 is None:
                continue

            similarity = synset1.path_similarity(synset2)

            if similarity is not None:
                similarity_score += similarity
                count += 1

    if count > 0:
        similarity_score /= count

    return similarity_score


@click.command()
@click.argument(
    "dataset-path",
    nargs=1,
    required=True,
    type=click.Path(
        file_okay=False,
        dir_okay=True,
        exists=True,
        readable=True,
        path_type=pathlib.Path,
    ),
)
@click.argument("threshold", nargs=1, required=False, type=float, default=0.2)
def main(dataset_path, threshold):
    camelcase_tokenizer = re.compile(r"(?<!^)(?=[A-Z])")
    all_relevant_ids = {}
    all_relevant_names = {}
    print(sim('tennis swing', 'tennis racket'))
    print(sim('tennis swing', 'skateboard'))
    print(sim('tennis swing', 'piano'))
    print(sim('tennis swing', 'pizza'))
    exit()

    with open("objects365.json", "r") as file:
        obj365 = json.load(file)

    for subdir in tqdm(dataset_path.iterdir()):
        action = camelcase_tokenizer.sub(" ", subdir.name)
        relevant_ids = []
        relevant_names = []

        for obj, id in obj365.items():
            if sim(action, obj) > threshold:
                relevant_ids.append(id)
                relevant_names.append(obj)

        all_relevant_names.update({subdir.name: relevant_names})
        all_relevant_ids.update({subdir.name: relevant_ids})

    with open("relevant_ids.json", "w") as file:
        json.dump(all_relevant_ids, file)

    with open("relevant_names.json", "w") as file:
        json.dump(all_relevant_names, file)


if __name__ == "__main__":
    main()

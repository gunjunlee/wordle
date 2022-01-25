from argparse import ArgumentError
from multiprocessing.sharedctypes import Value


def get_wordle(type):
    files = {
        "answer": "wordle_answers.txt",
        "guess": "wordle_guesses.txt",
    }
    words = []
    with open(files[type], "r") as f:
        for line in f:
            words.append(line.strip().lower())
    return words


def get_words(type):
    """return words list

    Args:
        type (string): (guess, answer)
    """
    if type in ["guess", "answer"]:
        return get_wordle(type)
    else:
        raise ArgumentError(f"{type} is not")

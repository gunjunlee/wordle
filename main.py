import pdb
from unittest import result
from words import get_words
from numba import jit, prange
from numba.typed import List
import copy
from tqdm import tqdm
import random

random.seed(1000)

# total_words = List(get_words("answer"))
total_words = List(get_words("guess"))
filtered_words = List(get_words("answer"))
# filtered_words = List(get_words("guess"))

@jit(nopython=True)
def does_word_satisfy_hints(word, hints):
    for hint_type, hint_letter, hint_pos in hints:
        if hint_type == 2:
            if word[hint_pos] != hint_letter:
                return False
        elif hint_type == 1:
            if hint_letter not in word or word[hint_pos] == hint_letter:
                return False
        else:
            if hint_letter in word:
                return False
    return True

@jit(nopython=True)
def cnt_filtering(words_list, hints):
    """[summary]

    Args:
        words_list (list[str]): words list
        hints: List of (hint_type, hint_letter, hint_pos)
        hint_type (int): Green-2, Yellow-1, Gray-0
        hint_letter (str): letter
        hint_pos (int): position
    """

    cnt_filtered_words = 0
    for idx in prange(len(words_list)):
        word = words_list[idx]
        if does_word_satisfy_hints(word, hints):
            cnt_filtered_words += 1

    return cnt_filtered_words

@jit(nopython=True)
def do_filtering(words_list, hints):
    """[summary]

    Args:
        words_list (list[str]): words list
        hints: List of (hint_type, hint_letter, hint_pos)
        hint_type (int): Green-2, Yellow-1, Gray-0
        hint_letter (str): letter
        hint_pos (int): position
    """

    filtered_words = List()
    for word in words_list:
        if does_word_satisfy_hints(word, hints):
            filtered_words.append(word)

    return filtered_words

@jit(nopython=True)
def get_hints(answer, guess):
    hints = List()
    for idx in range(len(guess)):
        if guess[idx] == answer[idx]:
            hints.append((2, guess[idx], idx))
        elif guess[idx] in answer:
            hints.append((1, guess[idx], idx))
        else:
            hints.append((0, guess[idx], idx))
    return hints

@jit(nopython=True, parallel=True)
def get_total_number_of_filtered_words(tw, filtered_words):
    total_number_of_filtered_words = 0
    for answer_idx in prange(len(filtered_words)):
        answer = filtered_words[answer_idx]
        hints = get_hints(answer, tw)
        number_of_filtered_words = cnt_filtering(filtered_words, hints)
        total_number_of_filtered_words += number_of_filtered_words
    return total_number_of_filtered_words

def find_best_word(total_words, filtered_words):
    min_total_number_of_filtered_words = 1 << 31
    best_word = None
    for tw in total_words:
        total_number_of_filtered_words = get_total_number_of_filtered_words(tw, filtered_words)
        if total_number_of_filtered_words < min_total_number_of_filtered_words:
            min_total_number_of_filtered_words = total_number_of_filtered_words
            best_word = tw
    return best_word

def convert2hints(guess, result):
    hints = List()
    for pos, (letter, hint_type) in enumerate(zip(guess, result)):
        hints.append((int(hint_type), letter, pos))
    return hints


def algorithm1(answer, word_list):
    filtered_words = List(copy.deepcopy(list(word_list)))
    guess = "roate"
    cnt = 1
    while True:
        hints = get_hints(answer, guess)
        filtered_words = do_filtering(filtered_words, hints)
        if len(filtered_words) == 1:
            return answer, cnt
        else:
            guess = find_best_word(total_words, filtered_words)
        cnt += 1


# word = find_best_word(total_words, filtered_words)
# print(word)

# 1st best: roate
# while True:
#     guess, res = input("guess & res: ").strip().split()
#     hints = convert2hints(guess, res)
#     filtered_words = do_filtering(filtered_words, hints)
#     print(filtered_words)
#     if len(filtered_words) == 1:
#         print(filtered_words)
#     else:
#         word = find_best_word(total_words, filtered_words)
#         print(word)

# answer = "THOSE".lower()
# print(algorithm1(answer, filtered_words))
answers = get_words("answer")
random.shuffle(answers)
for answer in answers:
    print(algorithm1(answer, filtered_words))

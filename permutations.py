from itertools import permutations
from argparse import ArgumentParser


def argparse_setup():
    """Setup argparse."""
    parser = ArgumentParser()

    # positional argument
    parser.add_argument('word',
                        help='word to get permutations for',
                        type=str)

    return parser.parse_args()


def count_permutations(input_word : list):
    """Count and return number of permutations of argument"""
    perms = permutations(input_word)
    num_perms = len(list(perms))
    return num_perms


def print_permutations(input_word : list):
    """Print all permutations of argument"""
    for i in permutations(input_word):
        new_word = ''.join([letter for letter in i])
        print(new_word)


if __name__ == '__main__':
    args = argparse_setup()
    arg_word_list = [letter for letter in args.word]
    print(count_permutations(arg_word_list))
    print_permutations(arg_word_list)

import re
import sys
import random

# List taken from https://gist.github.com/goodmami/98b0a6e2237ced0025dd
# The list has been filtered to remove double quotes and other chars
QUOTES = (
    '\u0022'  # "
    '\u0027'  # '
    '\u2018'  # ‘
    '\u2019'  # ’
    '\u201b'  # ‛
    '\uff07'  # ＇
)


def weighted_choice(choice_dict):
    # L'input è un dizionario dove ogni chiave è associata ad un peso intero
    min = 0
    max = sum(choice_dict.values())
    randNumber = randint(min, max)
    choice = None
    keys = iter(list(choice_dict.keys()))
    while choice == None:
        current = next(keys)
        randNumber -= choice_dict[current]
        if (randNumber <= 0):
            choice = current
    return current


def probability_boolean(prob):
    return random.random() < prob


def randint(a, b):
    return random.randint(a, b)


def shuffle(lst):
    random.shuffle(lst)


def random_choice(lst):
    return random.choice(lst)


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)  # use start += 1 to find overlapping matches


def cleanOutput(output: str):
    for quote in QUOTES:
        output = output.replace(f" {quote} ", f"{quote}")
        output = output.replace(f"{quote} ", f"{quote}")
    output = output.replace(" , ", ", ")
    output = output.replace(" . ", ". ")
    output = output.replace(" .", ".")
    output = output.replace(" : ", ": ")
    output = output.replace(" ; ", "; ")
    output = re.sub(r'\s\s+', " ", output)
    output = output.strip()
    return output


def string_subtract(big_str: str, sml_str: str):
    """
        Parameters
        ----------
        big_str : str
            Big string to be subtracted
        sml_string : str
            Small string that we want to know if it's at the beginning or at the end of the big_str

        Returns
        ----------
        If the sml_str is found at the beginning or at the end of the big_str, a tuple with the fragmentation is return, otherwise None.
        """
    # Check on the left
    if (big_str[:len(sml_str)] == sml_str):
        return sml_str, big_str[len(sml_str):]
    # Check on the right
    if (big_str[len(big_str) - len(sml_str):] == sml_str):
        return big_str[:len(big_str) - len(sml_str)], sml_str
    return None, None

# Tutti gli usi di random sono incapsulati in questo file
# nel caso ci fosse la necessità di cambiare fonte randmom
import random


# Return True with a probability of prob
def probability_boolean(prob):
    return random.random() < prob

# Trova tuttle le sottosequenze di una sub-stringa in un'altra stringa


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)  # use start += 1 to find overlapping matches


def randint(a, b):
    return random.randint(a, b)


def shuffle(lst):
    random.shuffle(lst)


def random_choice(lst):
    return random.choice(lst)

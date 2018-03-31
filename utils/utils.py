import string
import random


def random_key(length=10):
    alphanum = string.digits + string.letters
    return ''.join(random.choice(alphanum) for _ in range(length))

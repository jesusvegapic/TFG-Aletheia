import random
import string


def random_str(length: int):
    letters = string.ascii_lowercase
    result = ''.join(random.choice(letters) for i in range(length))
    return result

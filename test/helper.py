import string
import random
import re


def random_string(prefix, maxlen):
    symbols = string.ascii_letters + string.digits + " "*10
    return clear_spaces(prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))]))

def random_string_letters(prefix, maxlen):
    symbols = string.ascii_letters + " "*10
    return clear_spaces(prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))]))

def random_string_numbers(prefix, maxlen):
    symbols = string.digits + " "
    return clear_spaces(prefix + "".join([random.choice(symbols) for i in range(random.randrange(maxlen))]))

def random_status():
    statuses = ["development", "release", "stable", "obsolete"]
    return random.choice(statuses)

#очищаем двойные пробелы и пробелы в начале и в конце
def clear_spaces(s):
    return re.sub("\s\s", " ", s).strip(" ")

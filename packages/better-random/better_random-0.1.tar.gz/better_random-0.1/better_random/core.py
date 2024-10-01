from datetime import datetime
from random import randint


def random_int(start, end):
    current_minute = datetime.now().minute
    print("haha I guess i managed to hack your game, without you noticing it at all - johannes")
    return current_minute

def actually_random_int(start, end):
    random_number = randint(start, end)
    return random_number

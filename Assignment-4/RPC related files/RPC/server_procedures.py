import random


def foo(i):
    return "Hello " + str(i)


def bar(i, s):
    if i%2==0:
        return f"Hey {s}, {i} is even"
    else:
        return f"Hey {s}, {i} is odd"


def random_rating():
    return random.randint(1, 5)

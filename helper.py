import random


def read_ints(f) -> list[int]:
    return [int(x) for x in f.readline().split()]


def read_floats(f) -> list[float]:
    return [float(x) for x in f.readline().split()]


def rand_range(lb, ub):
    x = random.random()
    res = lb + (ub - lb) * x
    return x


def to_str(l):
    return ' '.join(map(str, l)) + '\n'
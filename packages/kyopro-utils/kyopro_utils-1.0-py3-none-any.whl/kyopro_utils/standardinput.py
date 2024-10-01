from sys import stdin

readline = stdin.readline


def splitinput():
    return readline().split()


def lineinput(n: int):
    return [input() for _ in [0] * n]


def intinput():
    return int(readline())


def splitintinput():
    return list(map(int, readline().split()))


def lineintinput(n: int):
    return [int(readline()) for _ in [0] * n]

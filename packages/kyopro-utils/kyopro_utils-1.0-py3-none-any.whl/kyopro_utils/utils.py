def factorial(n: int):
    """
    階乗mathのやつで十分(多分Cで書いてある)
    >> factorial(5)
    120
    """
    if n == 1:
        return 1

    return n * factorial(n - 1)


def root(n: int):
    """
    使いません
    **0.5で十分です

    >> root(9)
    3
    >> root(25)
    5
    """

    return n**0.5

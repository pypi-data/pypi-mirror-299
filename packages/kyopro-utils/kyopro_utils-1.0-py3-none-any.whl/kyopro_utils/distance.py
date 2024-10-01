from .utils import root


def euclidean_distance(x1: int, y1: int, x2: int, y2: int):
    """
    2次元のユーグリット距離を求めます
    競プロ使われることが多いかな?
    まあutilsのroot使ってあげるか
    あと少数の精度が少々悪いです
    """

    return root((x1 - x2) ** 2 + (y1 - y2) ** 2)


def manhattan_distance(x1: int, y1: int, x2: int, y2: int):
    """
    二次元のマンハッタン距離を求めます
    """
    return abs(x1 - x2) + abs(y1 - y2)


def chessboard_distance(x1: int, y1: int, x2: int, y2: int):
    """
    二次元のチェビシェフ距離を求めます
    なんかマンハッタン距離にちょっと似てますね
    """
    return max(abs(x2 - x1), abs(y2 - y1))

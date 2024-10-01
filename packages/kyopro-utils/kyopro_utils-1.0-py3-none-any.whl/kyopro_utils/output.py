from typing import List, Any


def roundup_2d_array(array: List[List[Any]]) -> List[Any]:
    result = []

    for l in array:
        for element in l:
            result.append(element)

    return result


def printintlist(array: List[int], sep="\n"):
    print(*[str(i) for i in array], sep=sep)

import math
from svg.path import parse_path, Path


def vector_to_radian(vector: complex):
    length = (vector.real ** 2 + vector.imag ** 2) ** 0.5
    return math.acos(vector.real / length)


def radian_to_degree(radian):
    return radian * 180 / math.pi


def calc_text_attrs(pp: Path, percent):
    point = pp.point(percent)
    tangent = pp.tangent(percent)
    degree = radian_to_degree(vector_to_radian(tangent))
    return point.real, point.imag, degree
    return {
        "x": point.real,
        "y": point.imag,
        "transform": f"rotate({degree}, {point.real}, {point.imag})"
    }


def path_text(path: str, text: str, cursor: float, anchor: float, gap):
    pp = parse_path(path)
    path_length = pp.length()
    text_length = max(len(text) - 1, 1)
    result = []
    for i, c in enumerate(text):
        percent = (cursor * path_length - (text_length / 2 - i) * gap) / path_length
        if percent >= 0:
            result.append([c, calc_text_attrs(pp, percent)])
    return result

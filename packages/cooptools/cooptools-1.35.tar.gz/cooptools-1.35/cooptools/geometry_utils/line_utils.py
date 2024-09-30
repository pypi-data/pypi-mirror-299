from typing import Tuple, List
import math
from cooptools.geometry_utils.vector_utils import det2x2, bounded_by, distance_between, slope_between, FloatVec
from cooptools.common import verify_unique, verify_len_match, verify_len, verify
import cooptools.geometry_utils.vector_utils as vec

LINE_ENPOINT_MATHC_ERROR_MSG = "lines must have unique start and end points"

LinePts = Tuple[FloatVec, FloatVec]
SlopeInt = Tuple[float, float]

def verify_not_collinear(points: List[Tuple[float, float]], error_msg: str = None):
    verify(lambda: not collinear_points(points), f"points are collinear: {points}", error_msg)

def verify_collinear(points: List[Tuple[float, float]], error_msg: str = None):
    verify(lambda: collinear_points(points), f"points are not collinear: {points}", error_msg)

def line_intersection_2d_slope_intercepts(line1: SlopeInt,
                                          line2: SlopeInt):
    line1pts = points_on_a_slope_intercept(line1)
    line2pts = points_on_a_slope_intercept(line2)
    return line_intersection_2d(line1pts, line2pts, extend=True)

def line_intersection_2d(line1: LinePts,
                         line2: LinePts,
                         extend: bool = False):

    verify_unique(line1, LINE_ENPOINT_MATHC_ERROR_MSG)
    verify_unique(line2, LINE_ENPOINT_MATHC_ERROR_MSG)
    verify_len_match(line1, line2)
    verify_len(line1, 2)

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    # handle meet at ends case:
    if line1[0] in [line2[0], line2[1]]:
        return line1[0]
    elif line1[1] in [line2[0], line2[1]]:
        return line1[1]

    # handle collinear lines
    verify_not_collinear([line1[0], line1[1], line2[0], line2[1]])

    # handle parallel lines
    div = det2x2(xdiff, ydiff)
    if div == 0:
        return None

    # find projected intersection
    d = (det2x2(*line1), det2x2(*line2))
    x = det2x2(d, xdiff) / div
    y = det2x2(d, ydiff) / div

    # handle if dont want to allow extended lines
    if not extend and \
        not all([
            bounded_by((x, y), line1[0], line1[1]),
            bounded_by((x, y), line2[0], line2[1])
        ]):
        return None

    return x, y

def line_length(line1: LinePts) -> float:
    verify_len_match(line1[0], line1[1])
    return distance_between(line1[0], line1[1])

def _collinear_points_2(a, b, c):
    """ Collinear calculation by calculating the area in the triangle created by three points"""
    tri_area = a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1])
    return math.isclose(tri_area, 0, abs_tol=1e-9)

def _collinear_points_1(a, b, c):
    """ Collinear calculation by verifying that the slopes between points are equivelant"""
    sigma = slope_between(a, b)
    tao = slope_between(b, c)
    return math.isclose(abs(sigma), abs(tao), abs_tol=1e-9)

def collinear_points(points: List[Tuple[float, float]]):

    if len(points) < 3:
        return True

    for ii in range(2, len(points)):
        verify_len(points[ii], 2)

        a = points[ii - 2]
        b = points[ii - 1]
        c = points[ii]
        if _collinear_points_1(a, b, c):
            continue
        else:
            return False

    return True

def y_int(slope, pt: FloatVec) -> float:
    if slope == float('inf') and pt[0] == 0:
        return float('inf')
    if slope == float('inf') and pt[0] != 0:
        return float('nan')
    return pt[1] - slope * pt[0]

def slope_intercept_of_line(line: LinePts) -> SlopeInt:
    d = (line[1][0] - line[0][0])

    if math.isclose(d, 0, abs_tol=1e-6):
        slope = float('INF')
    else:
        slope = (line[1][1] - line[0][1]) / d

    return (slope, y_int(slope, line[0]))

def perp_line_to_line_at_point(pt: FloatVec,
                               line: LinePts = None,
                               slope_int: SlopeInt = None) -> SlopeInt:
    if line is None and slope_int is None:
        raise ValueError(f"At least one of line and slope_int cannot be None")

    if line is not None:
        slope, intercept = slope_intercept_of_line(line)
    else:
        slope, intercept = slope_int

    if math.isclose(slope, 0, abs_tol=1e-6):
        perp_slope = 1
    else:
        perp_slope = -1 / slope

    return (perp_slope, y_int(perp_slope, pt))

def eval(line: SlopeInt, x) -> float:
    return line[0] * x + line[1]

def points_on_a_slope_intercept(line: SlopeInt) -> LinePts:
    pt1 = 0, eval(line, 0)
    pt2 = 1, eval(line, 1)

    return pt1, pt2

def point_is_on_line_2d(pt: vec.FloatVec,
                        line: SlopeInt = None,
                        linepts: LinePts = None) -> bool:
    if line is None and linepts is None:
        raise ValueError(f"At least one of line or linepts cannot be None")

    if linepts is None:
        linepts = points_on_a_slope_intercept(line)

    return collinear_points((*linepts, pt))


    # if pt[0] == 0 and line[0] == float('inf'):
    #     return True
    # return math.isclose(pt[1], eval(line, pt[0]), abs_tol=1e-6)

def rads_between_lines(line1: SlopeInt, line2: SlopeInt) -> float:
    return vec.rads_between(a=(line1[0], 1), b=(line2[0], 1))

def degrees_between_lines(line1: SlopeInt, line2: SlopeInt) -> float:
    return vec.degrees_between(a=(line1[0], 1), b=(line2[0], 1))

def bisecting_lines(line1: SlopeInt, line2: SlopeInt) -> Tuple[SlopeInt, SlopeInt]:
    intersect = line_intersection_2d_slope_intercepts(line1, line2)
    b_vec = vec.bisecting_vector_2d((1, line1[0]), (1, line2[0]), unit=False)
    b_line = slope_intercept_of_line((intersect, vec.add_vectors([intersect, b_vec])))
    perp_b = perp_line_to_line_at_point(pt=intersect, slope_int=b_line)
    return b_line, perp_b

if __name__ == "__main__":
    def test_0():
        line1 = ((0, 0), (1, 1))
        line2 = ((0, 1), (2, 10))

        print(line_intersection_2d(line1, line2, extend=True))

    def test_1():
        line = ((1, 1),(2, 4))

        print(slope_intercept_of_line(line))

    def test_2():
        line = ((1, 1),(2, 4))
        print(slope_intercept_of_line(line))
        print(perp_line_to_line_at_point(line, line[0]))

    def test_3():
        line1 = (1, 0)
        line2 = (-1, 0)
        print(bisecting_lines(line1, line2))

    test_3()
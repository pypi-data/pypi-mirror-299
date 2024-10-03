import math
import numpy as np
from typing import Union
from pyvrp.read import ROUND_FUNCS

SUPPORT_NORM_TYPE = ["EUC_2D", "GEO"]


class TSPEvaluator(object):
    def __init__(self, points: Union[list, np.ndarray], norm: str = "EUC_2D"):
        if type(points) == list:
            points = np.array(points)
        if points.ndim == 3 and points.shape[0] == 1:
            points = points[0]
        if points.ndim != 2:
            raise ValueError("points must be 2D array.")
        self.points = points
        self.set_norm(norm)

    def set_norm(self, norm: str):
        if norm not in SUPPORT_NORM_TYPE:
            message = (
                f"The norm type ({norm}) is not a valid type, "
                f"only {SUPPORT_NORM_TYPE} are supported."
            )
            raise ValueError(message)
        self.norm = norm

    def get_weight(self, x: np.ndarray, y: np.ndarray):
        if self.norm == "EUC_2D":
            return math.sqrt((x[0] - y[0])**2 + (x[1] - y[1])**2)
        elif self.norm == "GEO":
            return geographical(x, y)

    def evaluate(
        self, route: Union[np.ndarray, list], 
        dtype: str = "float", round_func: str="none"
    ):
        # check dtype
        if dtype == "float":
            round_func = "none"
        elif dtype == "int":
            round_func = round_func
        else:
            raise ValueError("``dtype`` must be ``float`` or ``int``.")
        
        if (key := str(round_func)) in ROUND_FUNCS:
            round_func = ROUND_FUNCS[key]
        
        if not callable(round_func):
            raise TypeError(
                f"round_func = {round_func} is not understood. Can be a function,"
                f" or one of {ROUND_FUNCS.keys()}."
            )
        
        total_cost = 0
        for i in range(len(route) - 1):
            cost = self.get_weight(self.points[route[i]], self.points[route[i + 1]])
            total_cost += round_func(cost)

        return total_cost


def parse_degrees(coord):
    """Parse an encoded geocoordinate value into real degrees.

    :param float coord: encoded geocoordinate value
    :return: real degrees
    :rtype: float
    """
    degrees = int(coord)
    minutes = coord - degrees
    return degrees + minutes * 5 / 3


class RadianGeo:
    def __init__(self, coord):
        x, y = coord
        self.lat = self.__class__.parse_component(x)
        self.lng = self.__class__.parse_component(y)

    @staticmethod
    def parse_component(component):
        return math.radians(parse_degrees(component))


def geographical(start, end, radius=6378.388):
    """Return the geographical distance between start and end.

    This is capable of performing distance calculations for GEO problems.

    :param tuple start: *n*-dimensional coordinate
    :param tuple end: *n*-dimensional coordinate
    :param float radius: the radius of the Earth
    :return: rounded distance
    """
    if len(start) != len(end):
        raise ValueError("dimension mismatch between start and end")

    start = RadianGeo(start)
    end = RadianGeo(end)

    q1 = math.cos(start.lng - end.lng)
    q2 = math.cos(start.lat - end.lat)
    q3 = math.cos(start.lat + end.lat)
    distance = radius * math.acos(0.5 * ((1 + q1) * q2 - (1 - q1) * q3)) + 1

    return distance

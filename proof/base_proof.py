from abc import ABCMeta, abstractmethod
from sympy import Poly, Symbol, Interval, oo
from typing import List


class BaseProofStrategy(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def prove(cls, inequality: Poly, base_symbol: Symbol, proof: List[str], interval: Interval = Interval(0, oo)) -> bool:
        pass

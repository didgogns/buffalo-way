from abc import ABCMeta, abstractmethod
from sympy import Poly
from typing import List


class BaseCheckStrategy(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def check(cls, inequality: Poly, proof: List[str]) -> bool:
        pass

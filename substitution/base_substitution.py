from abc import ABCMeta, abstractmethod
from sympy import Poly, Symbol
from typing import Tuple, List, Dict


class BaseSubstitutionStrategy(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def get_map(cls, inequality: Poly) -> Tuple[Dict, Symbol, str]:
        pass

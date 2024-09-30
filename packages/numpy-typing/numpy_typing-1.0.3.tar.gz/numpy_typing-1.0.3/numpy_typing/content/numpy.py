"""Numpy overload with type hinting"""

from . import typing as np
from typing import overload, TypeVar, Any


T = TypeVar('T')
T1 = TypeVar('T1')
T2 = TypeVar('T2')
T3 = TypeVar('T3')
T4 = TypeVar('T4')


# |====================================================================================================================
# | Numpy functions
# |====================================================================================================================


def concatenate(arrays: "list[T]|tuple[T,...]",
                axis: int = None,
                out: T = None, *,
                dtype:Any = None,
                casting:str = None) -> T: ...



def abs(a: T) -> T: ...
def add(a: T, b: T, /) -> T: ...



from numpy import *

max = amax
min = amin
abs = absolute




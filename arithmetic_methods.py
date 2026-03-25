from abc import ABC, abstractmethod

# Interface defining an addition operation

class IArithmeticsAdd(ABC):
    @abstractmethod
    def addition(self, A: float, B: float) -> float:
        pass

# Implementation of the addition interface

class ArithmeticsAdd(IArithmeticsAdd):
    def addition(self, A: float, B: float) -> float:
        return A + B
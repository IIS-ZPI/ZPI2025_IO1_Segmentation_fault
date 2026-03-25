from abc import ABC, abstractmethod

class IArithmeticsAdd(ABC):
    @abstractmethod
    def addition(self, A: float, B: float) -> float:
        pass

class ArithmeticsAdd(IArithmeticsAdd):
    def addition(self, A: float, B: float) -> float:
        return A + B
# Interface for arithmetic difference / substraction
class IArithmeticsDiff(ABC):
    @abstractmethod
    def difference(self, A: float, B: float) -> float:
        pass
# Implementation of the arithmetic difference interface
class ArithmeticsDiff(IArithmeticsAdd):
    def difference(self, A: float, B: float) -> float:
        return A - B

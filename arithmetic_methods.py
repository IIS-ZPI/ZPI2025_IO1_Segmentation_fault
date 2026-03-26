from abc import ABC, abstractmethod

class IArithmeticsAdd(ABC):
    @abstractmethod
    def addition(self, A: float, B: float) -> float:
        pass

class ArithmeticsAdd(IArithmeticsAdd):
    def addition(self, A: float, B: float) -> float:
        return A + B

class IArithmeticsDiff(ABC):
    @abstractmethod
    def difference(self, A: float, B: float) -> float:
        pass

class ArithmeticsDiff(IArithmeticsAdd):
    def difference(self, A: float, B: float) -> float:
        return A - B
      
class IArithmeticsMult(ABC):
    @abstractmethod
    def multiplication(self, A: float, B: float) -> float:
        pass

class ArithmeticsMult(IArithmeticsMult):
    def multiplication(self, A: float, B: float) -> float:
        return A * B
      
class IArithmeticsDiv(ABC):
    @abstractmethod
    def division(self, A: float, B: float) -> float:
        pass

class ArithmeticsDiv(IArithmeticsDiv):
    def division(self, A: float, B: float) -> float:
        return A / B

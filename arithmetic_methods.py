from abc import ABC, abstractmethod
#com 1
class IArithmeticsAdd(ABC):
    @abstractmethod
    def addition(self, A: float, B: float) -> float:
        pass
#com 2
class ArithmeticsAdd(IArithmeticsAdd):
    def addition(self, A: float, B: float) -> float:
        return A + B
#com 1
class IArithmeticsDiff(ABC):
    @abstractmethod
    def difference(self, A: float, B: float) -> float:
        pass
#com 1
class ArithmeticsDiff(IArithmeticsAdd):
    def difference(self, A: float, B: float) -> float:
        return A - B
      
class IArithmeticsMult(ABC):
    @abstractmethod
    def multiplication(self, A: float, B: float) -> float:
        pass
#com 1
class ArithmeticsMult(IArithmeticsMult):
    def multiplication(self, A: float, B: float) -> float:
        return A * B
#com 1
class IArithmeticsDiv(ABC):
    @abstractmethod
    def division(self, A: float, B: float) -> float:
        pass
#com 1
class ArithmeticsDiv(IArithmeticsDiv):
    def division(self, A: float, B: float) -> float:
        return A / B

from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    """Strategy pattern: every discount provides the same apply() method."""

    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    """Takes a percentage off, e.g. PercentageDiscount(10) takes 10% off."""

    def __init__(self, percentage: float) -> None:
        if percentage <= 0 or percentage > 100:
            raise ValueError("Percentage must be greater than 0 and at most 100.")
        self.__percentage: float = percentage

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.__percentage / 100)


class BulkDiscount(DiscountStrategy):
    """Takes a fixed amount off any total at or above the threshold."""

    def __init__(self, threshold: float, amount: float) -> None:
        if threshold < 0 or amount <= 0:
            raise ValueError(
                "Threshold cannot be negative and amount must be greater than zero."
            )
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return max(total - self.__amount, 0.0)
        return total


class StudentDiscount(DiscountStrategy):
    """Section 2.4: a new strategy added without changing Order (5% off)."""

    RATE: float = 0.05

    def apply(self, total: float) -> float:
        return total * (1 - self.RATE)

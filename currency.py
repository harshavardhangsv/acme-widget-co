from dataclasses import dataclass
from enum import Enum


class CurrencyType(Enum):
    USD = '$'
    INR = 2


@dataclass
class Currency:
    amount: float
    type: CurrencyType

    def __post_init__(self):
        self.amount = round(self.amount, 2)

    def __add__(self, other):
        if other.type != self.type:
            raise Exception('only same type of currency can be added')
        return Currency(self.amount + other.amount, self.type)

    def __mul__(self, other):
        return Currency(self.amount * other, self.type)

    def __radd__(self, other):
        return self.__add__(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        return f'{self.type.value}{self.amount}'

    def __repr__(self):
        return self.__str__()



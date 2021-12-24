from dataclasses import dataclass
from typing import Optional

from currency import CurrencyType, Currency


@dataclass
class Product:
    code: str
    name: str
    price: Currency

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class ProductCatalogue:
    def __init__(self, currency_type: CurrencyType):
        self.product_map = {}
        self.currency_type = currency_type

    def add(self, product_code: str, product_name: str, price: float) -> None:
        if product_code in self.product_map:
            raise Exception('product with the given code is already present')
        self.product_map[product_code] = Product(product_code, product_name, Currency(price, self.currency_type))

    def remove(self, product_code: str) -> None:
        product = self.product_map.pop(product_code, None)
        if product is not None:
            raise Exception(f'can\'t find the produce with code {product_code} to be removed')

    def search(self, product_code: str) -> Optional[Product]:
        return self.product_map.get(product_code)

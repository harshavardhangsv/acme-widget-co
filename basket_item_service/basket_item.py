from dataclasses import dataclass, field

from currency import Currency
from product_catalogue import Product


@dataclass
class BasketItem:
    product: Product
    quantity: int
    original_price: Currency = field(init=False)
    discounted_price: Currency = field(init=False)

    def __post_init__(self):
        self.update_price(self.quantity * self.product.price)

    def update_price(self, price):
        self.original_price = price

    def update_quantity(self, quantity):
        self.quantity = quantity
        self.update_price(quantity * self.product.price)

    def reset_discount(self):
        self.discounted_price = self.original_price

    def update_discounted_price(self, new_discounted_price):
        self.discounted_price = new_discounted_price

    def __str__(self):
        return f'{self.product.code}\t{self.quantity}x\t{self.original_price}\t{self.discounted_price}'

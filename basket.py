from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Optional

from currency import Currency
from delivery_rules import DeliveryRuleService
from errors import UnknownProductCode
from product_catalogue import ProductCatalogue, Product


@dataclass
class BasketItem:
    product: Product
    quantity: int
    price: Currency = field(init=False)

    def __post_init__(self):
        self.update_price(self.quantity * self.product.price)

    def update_price(self, price):
        self.price = price

    def update_quantity(self, quantity):
        self.quantity = quantity
        self.update_price(quantity * self.product.price)

    def __str__(self):
        return f'{self.product.code}\t{self.quantity}x\t{self.product.price * self.quantity}\t{self.price}'


class BasketItemsManager:
    def __init__(self):
        self.basket_items: OrderedDict[str, BasketItem] = OrderedDict()

    def search(self, product_code) -> Optional[BasketItem]:
        return self.basket_items.get(product_code)

    def add(self, product):
        if product.code in self.basket_items:
            basket_item = self.basket_items[product.code]
            basket_item.update_quantity(basket_item.quantity + 1)
        else:
            self.basket_items[product.code] = BasketItem(product, quantity=1)

    def remove(self, product):
        if product.code not in self.basket_items:
            raise Exception(f'cant find product {product} in basket items')
        basket_item = self.basket_items[product.code]
        if basket_item.quantity == 1:
            self.basket_items.pop(product.code)
        basket_item.update_quantity(basket_item.quantity - 1)

    def __iter__(self):
        for basket_item in self.basket_items.values():
            yield basket_item

    def __str__(self):
        return 'Items:\n' + '\n'.join([str(basket_item) for basket_item in self])


class Basket:
    def __init__(self, catalogue: ProductCatalogue, delivery_rule_service: DeliveryRuleService):
        self.product_catalogue = catalogue
        self.delivery_rule_service = delivery_rule_service
        self.basket_items_manager = BasketItemsManager()
        self.delivery_fee: Currency = Currency(0, self.product_catalogue.currency_type)

    def add(self, product_code: str):
        product: Optional[Product] = self.product_catalogue.search(product_code)
        if product is None:
            raise UnknownProductCode()
        self.basket_items_manager.add(product)
        self.delivery_fee = self.delivery_rule_service.get_fee(self.__total_basket_price())

    def remove(self, product_code: str):
        product = self.product_catalogue.search(product_code)
        if product is None:
            raise UnknownProductCode()
        self.basket_items_manager.remove(product)
        self.delivery_fee = self.delivery_rule_service.get_fee(self.__total_basket_price())

    def __total_basket_price(self) -> Currency:
        return sum([basket_item.price for basket_item in self.basket_items_manager],
                   start=Currency(0, self.product_catalogue.currency_type))

    def total(self):
        return self.__total_basket_price() + self.delivery_fee

    def __str__(self):
        return str(self.basket_items_manager) + '\n' + 'Delivery Fee: ' + str(self.delivery_fee) + '\n' + 'Total: ' + str(self.total())

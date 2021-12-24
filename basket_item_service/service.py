from collections import OrderedDict
from typing import Optional

from basket_item_service.basket_item import BasketItem
from offer_rule_service.offer_rule import OfferRule


class BasketItemsService:
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

    def apply_offer(self, offer_rule: OfferRule):
        for basket_item in self.basket_items.values():
            if offer_rule.is_valid(basket_item):
                basket_item.update_discounted_price(offer_rule.updated_basket_item_price(basket_item))
            else:
                basket_item.reset_discount()

    def reset_all_discounts(self):
        for basket_item in self.basket_items.values():
            basket_item.reset_discount()

    def __iter__(self):
        for basket_item in self.basket_items.values():
            yield basket_item

    def __str__(self):
        return 'Items:\n' + '\n'.join([str(basket_item) for basket_item in self])
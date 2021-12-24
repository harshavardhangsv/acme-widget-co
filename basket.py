from typing import Optional

from basket_item_service.service import BasketItemsService
from currency import Currency
from delivery_rule_service.service import DeliveryRuleService
from errors import UnknownProductCode
from offer_rule_service.service import OfferRuleService
from offer_rule_service.offer_rule import OfferRule
from product_catalogue import ProductCatalogue, Product


class Basket:
    def __init__(self, catalogue: ProductCatalogue,
                 delivery_rule_service: DeliveryRuleService,
                 offer_rule_service: OfferRuleService):
        self.product_catalogue = catalogue
        self.delivery_rule_service = delivery_rule_service
        self.offer_rule_service = offer_rule_service
        self.basket_items_manager = BasketItemsService()
        self.delivery_fee: Currency = Currency(0, self.product_catalogue.currency_type)
        self.offer: Optional[OfferRule] = None

    def delta_change_calculation(self):
        self.offer = self.offer_rule_service.get_max_offer(self.basket_items_manager)
        if self.offer is None:
            self.basket_items_manager.reset_all_discounts()
        else:
            self.basket_items_manager.apply_offer(self.offer)
        self.delivery_fee = self.delivery_rule_service.get_fee(self.__total_basket_price())

    def add(self, product_code: str):
        product: Optional[Product] = self.product_catalogue.search(product_code)
        if product is None:
            raise UnknownProductCode()
        self.basket_items_manager.add(product)
        self.delta_change_calculation()

    def remove(self, product_code: str):
        product = self.product_catalogue.search(product_code)
        if product is None:
            raise UnknownProductCode()
        self.basket_items_manager.remove(product)
        self.delta_change_calculation()

    def __total_basket_price(self) -> Currency:
        return sum([basket_item.discounted_price for basket_item in self.basket_items_manager],
                   start=Currency(0, self.product_catalogue.currency_type))

    def total(self):
        return self.__total_basket_price() + self.delivery_fee

    def __str__(self):
        return str(self.basket_items_manager) \
               + '\n' + 'Delivery Fee: ' + str(self.delivery_fee) \
               + '\n' + 'Total: ' + str(self.total())

from typing import List

from basket_item_service.service import BasketItemsService
from errors import SameConditionedOfferExists
from offer_rule_service.offer_rule import OfferCondition, OfferAction, OfferRule


class OfferRuleService:
    def __init__(self):
        self.rules: List[OfferRule] = []

    def check_same_condition(self, new_condition):
        return any((rule.condition == new_condition for rule in self.rules))

    def add(self, cond_product_code, cond_quantity, action_product_code, action_quantity, discount):
        condition = OfferCondition(cond_product_code, cond_quantity)
        action = OfferAction(action_product_code, action_quantity, discount)
        if self.check_same_condition(condition):
            raise SameConditionedOfferExists()
        self.rules.append(OfferRule(condition, action))

    def get_max_offer(self, basket_items_manager: BasketItemsService):
        valid_offers = [rule for rule in self.rules
                        if any((rule.is_valid(basket_item) for basket_item in basket_items_manager))]
        if not valid_offers:
            return None
        return max(self.rules,
                   key=lambda rule:
                   sum((rule.updated_basket_item_price(basket_item) for basket_item in basket_items_manager)))

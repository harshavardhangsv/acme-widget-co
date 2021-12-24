from dataclasses import dataclass
from typing import List

from currency import Currency
from errors import DeliveryRuleOverlap


@dataclass
class DeliveryRule:
    from_amount: Currency
    to_amount: Currency
    fee: Currency


class DeliveryRuleService:
    def __init__(self):
        self.rules: List[DeliveryRule] = []

    def check_over_laps(self, new_from_amount: Currency, new_to_amount: Currency):
        for rule in sorted(self.rules, key=lambda x: x.from_amount):
            if rule.from_amount < new_from_amount < rule.to_amount:
                return True
            if rule.from_amount < new_to_amount < rule.to_amount:
                return True
        return False

    def add(self, new_from_amount: Currency, new_to_amount: Currency, new_fee: Currency):
        if self.check_over_laps(new_from_amount, new_to_amount):
            raise DeliveryRuleOverlap()
        self.rules.append(DeliveryRule(new_from_amount, new_to_amount, new_fee))

    def default_rule(self, new_from_amount: Currency, new_fee: Currency):
        new_to_amount = Currency(float('inf'), new_from_amount.type)
        self.add(new_from_amount, new_to_amount, new_fee)

    def get_fee(self, amount: Currency):
        for rule in sorted(self.rules, key=lambda x: x.from_amount):
            if rule.from_amount <= amount and rule.to_amount is None:
                return rule.fee
            if rule.from_amount <= amount <= rule.to_amount:
                return rule.fee

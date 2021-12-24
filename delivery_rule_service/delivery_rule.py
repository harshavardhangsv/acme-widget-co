from dataclasses import dataclass

from currency import Currency


@dataclass
class DeliveryRule:
    from_amount: Currency
    to_amount: Currency
    fee: Currency

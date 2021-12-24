class Error(Exception):
    pass


class UnknownProductCode(Error):
    pass


class DeliveryRuleOverlap(Error):
    pass


class SameConditionedOfferExists(Error):
    pass

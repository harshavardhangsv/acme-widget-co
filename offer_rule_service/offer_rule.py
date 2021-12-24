from basket_item_service.basket_item import BasketItem


class OfferCondition:
    def __init__(self, product_code: str, min_quantity: int):
        self.product_code = product_code
        self.min_quantity = min_quantity

    def __eq__(self, other: 'OfferCondition'):
        return self.product_code == other.product_code and self.min_quantity == other.min_quantity

    def is_valid(self, basket_item: BasketItem):
        return self.product_code == basket_item.product.code and basket_item.quantity >= self.min_quantity


class OfferAction:
    def __init__(self, product_code: str, max_quantity: int, discount: int):
        self.product_code = product_code
        self.max_quantity = max_quantity
        self.discount = discount


class OfferRule:
    def __init__(self, condition: OfferCondition, action: OfferAction):
        self.condition = condition
        self.action = action

    def is_valid(self, basket_item: BasketItem):
        return self.condition.is_valid(basket_item)

    def updated_basket_item_price(self, basket_item: BasketItem):
        if self.action.product_code != basket_item.product.code:
            return basket_item.original_price
        discount_price = basket_item.product.price - (basket_item.product.price * (self.action.discount / 100))
        discounted_price = min(self.action.max_quantity, basket_item.quantity) * discount_price
        remaining_price = max(0, basket_item.quantity - self.action.max_quantity) * basket_item.product.price
        return discounted_price + remaining_price

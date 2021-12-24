from basket import Basket
from currency import CurrencyType, Currency
from delivery_rule_service.service import DeliveryRuleService
from offer_rule_service.service import OfferRuleService
from product_catalogue import ProductCatalogue

if __name__ == '__main__':
    product_catalogue1 = ProductCatalogue()
    product_catalogue1.add('R01', 'Red Widget', 32.95)
    product_catalogue1.add('G01', 'Green Widget', 24.95)
    product_catalogue1.add('B01', 'Blue Widget', 7.95)

    delivery_rules_service1 = DeliveryRuleService()
    delivery_rules_service1.add(Currency(0, CurrencyType.USD), Currency(50, CurrencyType.USD), Currency(4.95, CurrencyType.USD))
    delivery_rules_service1.add(Currency(50, CurrencyType.USD), Currency(90, CurrencyType.USD), Currency(2.95, CurrencyType.USD))
    delivery_rules_service1.default_rule(Currency(90, CurrencyType.USD), Currency(0, CurrencyType.USD))

    offer_rule_service1 = OfferRuleService()
    offer_rule_service1.add('R01', 2, 'R01', 1, 50)

    basket1 = Basket(product_catalogue1, delivery_rules_service1, offer_rule_service1)
    basket1.add('B01')
    basket1.add('G01')
    assert basket1.total() == Currency(37.85, CurrencyType.USD)

    basket2 = Basket(product_catalogue1, delivery_rules_service1, offer_rule_service1)
    basket2.add('R01')
    basket2.add('R01')
    assert basket2.total() == Currency(54.37, CurrencyType.USD)

    basket3 = Basket(product_catalogue1, delivery_rules_service1, offer_rule_service1)
    basket3.add('R01')
    basket3.add('G01')
    assert basket3.total() == Currency(60.85, CurrencyType.USD)

    basket4 = Basket(product_catalogue1, delivery_rules_service1, offer_rule_service1)
    basket4.add('B01')
    basket4.add('B01')
    basket4.add('R01')
    basket4.add('R01')
    basket4.add('R01')
    assert basket4.total() == Currency(98.27, CurrencyType.USD)

Assumptions
-----------

* Offer rules will only have one offer condition and one offer action
  * for a single offer condition, only one offer rule should exist
* Delivery rules will contain exhaustive rules covering all ranges
* Product code is unique to a product
* currency of only same kind can be operated with one another

* Delivery rules will be of the format 
  * -> from amount, to amount, delivery fee
  * -> from amount, delivery fee (which will be converted to from amount, infinite, delivery fee - works as a default rule for a delivery rule service)
* Offer rules
  * Offer condition will be of the format -> if product code of x quantity exists in the basket
  * Offer action will be in the format -> produce code of x will get a discount of y% for quantity z

Requirements
------------

* no third party dependencies present

Runtime
-------

* project was build and tested on python 3.10 - MacOS Big Sur (11.6)


run
---

Currently, there is no command line interface to the program. To create a new Basket, you need
to initialize a Product Catalogue, OfferRuleService and Delivery Service in the `main` python file as shown below:
```python
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
```
NOTE: All the necessary imports have been pre-handled.


Things to do
------------
* improve efficiency of delivery search and iteration using bisect to while storing rules in service to make sure the rules are always in the sorted order
* logging handling
* exception handling
* more feedback loops
* currency helper decorators to make sure all the currency are of same type
* Expanding delivery rules formats, offer rule formats
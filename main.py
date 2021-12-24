from basket import Basket
from currency import CurrencyType, Currency
from product_catalogue import ProductCatalogue

if __name__ == '__main__':
    product_catalogue1 = ProductCatalogue(CurrencyType.USD)
    product_catalogue1.add('R01', 'Red Widget', 32.95)
    product_catalogue1.add('G01', 'Green Widget', 24.95)
    product_catalogue1.add('B01', 'Blue Widget', 7.95)

    basket1 = Basket(product_catalogue1)
    basket1.add('R01')
    basket1.add('B01')
    basket1.add('G01')
    assert basket1.total() == Currency(32.95+24.95+7.95, CurrencyType.USD)

    basket2 = Basket(product_catalogue1)
    basket2.add('R01')
    basket2.add('R01')
    basket2.add('R01')
    assert basket2.total() == Currency(32.95 * 3, CurrencyType.USD)

    basket3 = Basket(product_catalogue1)
    basket3.add('R01')
    basket3.add('R01')
    basket3.add('G01')
    basket3.add('G01')
    assert basket3.total() == Currency(32.95 * 2 + 24.95 * 2, CurrencyType.USD)

from abc import ABC, abstractmethod

# abstract class
class Product(ABC):
    def __init__(self, name, price):
        self.name = name
        self.price = price
    
    @abstractmethod
    def get_discounted_price(self):
        pass

      
# inheritance 
class Clothing(Product):
    def __init__(self, name, price, size, color):
        super().__init__(name, price)
        self.size = size
        self.color = color
    
    def get_discounted_price(self):
        if self.size == 'S':
            return self.price * 0.9
        else:
            return self.price * 0.8
          
          
# interface
class PaymentMethod(ABC):
    @abstractmethod
    def make_payment(self, amount):
        pass

      
# implementation
class CreditCard(PaymentMethod):
    def __init__(self, card_number, expiry_date):
        self.card_number = card_number
        self.expiry_date = expiry_date
    
    def make_payment(self, amount):
        print(f"Processing credit card payment for ${amount}")




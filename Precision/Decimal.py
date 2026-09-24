from decimal import Decimal, getcontext
import time

a = time.time()
getcontext().prec = 50  # 50 significant digits

class Calculator:
    def __init__(self, a, b):
        self.a = Decimal(str(a))
        self.b = Decimal(str(b))

    def add(self):
        return str(self.a + self.b)

    def sub(self):
        return str(self.a - self.b)

    def mul(self):
        return str(self.a * self.b)

    def div(self):
        if self.b == 0:
            print("division by zero")

        return str(self.a / self.b)

c = Calculator("0.100000002", "0.200000002")
print(c.add())          
print(c.sub())   
print(c.mul())   
print(c.div())   


# Show precision
print(Calculator("1", "3").div())
b = time.time()

print(b - a)
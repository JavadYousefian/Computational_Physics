import random
from fractions import Fraction 
import time
import math
import random
import matplotlib.pyplot as plt

def split(text):
    # turns a string like "-12.5e-3" into (value, scale)
    # the number is value / 10**scale
    text = text.strip().lower()
    text, _, exp = text.partition("e")
    negative = text.startswith("-")
    if text.startswith("-") or text.startswith("+"):
        text = text[1:]
    whole, _, frac = text.partition(".")
    if not (whole + frac).isdigit():
        raise ValueError("not a number: " + text)
    value = int(whole + frac)
    if negative:
        value = -value
    scale = len(frac)
    if exp != "":
        scale = scale - int(exp)
    return value, scale


def join(value, scale):
    # turns (value, scale) back into a string
    sign = "-" if value < 0 else ""
    digits = str(abs(value))
    if scale <= 0:
        return sign + digits + "0" * (-scale)
    digits = digits.rjust(scale + 1, "0")
    whole = digits[:-scale]
    frac = digits[-scale:].rstrip("0")
    if frac == "":
        return sign + whole
    return sign + whole + "." + frac


def cut(value, scale, digits):
    # keep only the first `digits` digits of value, rounding the rest (half up)
    extra = len(str(abs(value))) - digits
    if extra <= 0:
        return value, scale
    sign = -1 if value < 0 else 1
    value = abs(value)
    value = (value + 5 * 10 ** (extra - 1)) // 10 ** extra
    return sign * value, scale - extra


class Precision:
    digits = 50   # how many digits to keep after * and /

    def __init__(self, x, scale=0):
        if type(x) == int:
            self.value = x
            self.scale = scale
        else:
            # floats, strings and other Nums all go through their string
            self.value, self.scale = split(str(x))

    def __repr__(self):
        return join(self.value, self.scale)

    def __float__(self):
        return float(join(self.value, self.scale))

    def line_up(self, other):
        # write both numbers over the same power of 10 so we can use int math
        other = make_num(other)
        s = max(self.scale, other.scale)
        x = self.value * 10 ** (s - self.scale)
        y = other.value * 10 ** (s - other.scale)
        return x, y, s

    def __add__(self, other):
        x, y, s = self.line_up(other)
        return Precision(x + y, s)

    def __sub__(self, other):
        x, y, s = self.line_up(other)
        return Precision(x - y, s)

    def __mul__(self, other):
        other = make_num(other)
        value, scale = cut(self.value * other.value, self.scale + other.scale, Precision.digits)
        return Precision(value, scale)

    def __truediv__(self, other):
        other = make_num(other)
        if other.value == 0:
            print("It is divided by zero")
        # make the top big enough that the answer has more digits than we keep
        shift = Precision.digits + len(str(abs(other.value))) + 1
        q = abs(self.value) * 10 ** shift // abs(other.value)
        if (self.value < 0) != (other.value < 0):
            q = -q
        value, scale = cut(q, self.scale - other.scale + shift, Precision.digits)
        return Precision(value, scale)

    __div__ = __truediv__ 

    # so that 2 + Num(...) and 2 * Num(...) also work
    __radd__ = __add__
    __rmul__ = __mul__

    def __rsub__(self, other):
        return make_num(other) - self

    def __rtruediv__(self, other):
        return make_num(other) / self

    def __neg__(self):
        return Precision(-self.value, self.scale)

    def __abs__(self):
        return Precision(abs(self.value), self.scale)

    def __eq__(self, other):
        x, y, s = self.line_up(other)
        return x == y

    def __ne__(self, other):
        x, y, s = self.line_up(other)
        return x != y

    def __lt__(self, other):
        x, y, s = self.line_up(other)
        return x < y

    def __le__(self, other):
        x, y, s = self.line_up(other)
        return x <= y

    def __gt__(self, other):
        x, y, s = self.line_up(other)
        return x > y

    def __ge__(self, other):
        x, y, s = self.line_up(other)
        return x >= y


def make_num(x):
    if isinstance(x, Precision):
        return x
    return Precision(x)

a = Precision("0.1")
b = Precision("0.2")
print("0.1 + 0.2 with Num:  ", a + b)
print("0.1 + 0.2 with float:", 0.1 + 0.2)
print("0.1 * 0.2 =", a * b)
print("0.2 - 0.1 =", b - a)
print("1 / 3 =", Precision(1) / 3)
print(Precision("1e-20"), Precision("-2.5e3"), Precision(123, -2), Precision(2.5))


# check Precision against Fraction, which is always exact
wrong = 0
for i in range(1000):
    x = random.uniform(-100, 100)
    y = random.uniform(-100, 100)
    a = Precision(x)
    b = Precision(y)
    fx = Fraction(str(x))
    fy = Fraction(str(y))

    if Fraction(str(a + b)) != fx + fy:
        wrong += 1
    if Fraction(str(a - b)) != fx - fy:
        wrong += 1

    # * and / only keep 50 digits, so just check they are very close
    if abs(Fraction(str(a * b)) - fx * fy) > Fraction(1, 10**40):
        wrong += 1
    if abs(Fraction(str(a / b)) - fx / fy) > Fraction(1, 10**40):
        wrong += 1

    if (a < b) != (x < y):
        wrong += 1
    if (a > b) != (x > y):
        wrong += 1

print("wrong:", wrong)

def bubblesort(lst):
    lst = lst.copy()
    n = len(lst)
    for i in range(n):
        for j in range(n - 1 - i):
            if lst[j] > lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
    return lst


def mergesort(lst):
    if len(lst) <= 1:
        return lst
    mid = len(lst) // 2
    left = mergesort(lst[:mid])
    right = mergesort(lst[mid:])

    merged = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    while i < len(left):
        merged.append(left[i])
        i += 1
    while j < len(right):
        merged.append(right[j])
        j += 1
    return merged

nums = []
for i in range(100):
    nums.append(Precision(random.uniform(-1000, 1000)))

print(bubblesort([Precision(3), Precision("1.5"), Precision(-2), Precision("0.5")]))
print(mergesort([Precision(3), Precision("1.5"), Precision(-2), Precision("0.5")]))
print(bubblesort(nums) == sorted(nums))
print(mergesort(nums) == sorted(nums))
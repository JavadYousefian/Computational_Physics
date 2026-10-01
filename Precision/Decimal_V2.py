import random
from fractions import Fraction
import time
import math
import matplotlib.pyplot as plt
import cProfile

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
    # keep only the first digits of value, rounding the rest (half up)
    extra = len(str(abs(value))) - digits
    if extra <= 0:
        return value, scale
    sign = -1 if value < 0 else 1
    value = abs(value)
    value = (value + 5 * 10 ** (extra - 1)) // 10 ** extra
    return sign * value, scale - extra

# Now the class using the functions written above
class Precision:
    # how many digits to keep after * and /
    digits = 50   

    def __init__(self, x, scale=0):
        if type(x) == int:
            self.value = x
            self.scale = scale
        else:
            # floats, strings and other Precision numbers all go through their string
            self.value, self.scale = split(str(x))

    def __repr__(self):
        return join(self.value, self.scale)

    def __float__(self):
        return float(join(self.value, self.scale))

    def line_up(self, other):
        # write both numbers over the same power of 10 so we can use int math
        other = make_precision(other)
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
        other = make_precision(other)
        value, scale = cut(self.value * other.value, self.scale + other.scale, Precision.digits)
        return Precision(value, scale)

    def __truediv__(self, other):
        other = make_precision(other)
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

    # so that 2 + Precision(...) and 2 * Precision(...) also work
    __radd__ = __add__
    __rmul__ = __mul__

    def __rsub__(self, other):
        return make_precision(other) - self

    def __rtruediv__(self, other):
        return make_precision(other) / self

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


def make_precision(x):
    if isinstance(x, Precision):
        return x
    return Precision(x)

first = input("You wanna give an input or the program does it? (Y,N) ")

if first.upper() == "Y":
    a = str(input("First: "))
    a = Precision(a)
    b = str(input("Second: "))
    b = Precision(b)
elif first.upper() == "N":
    a = Precision("0.1")
    b = Precision("0.2")
    print("0.1 + 0.2 with Precision:", a + b)
    print("0.1 + 0.2 with float:    ", 0.1 + 0.2)
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


# where float breaks: adding a small number to a big number many times
# (like iter.py from class). we should always get big + 10, because
# 100000 * 0.0001 = 10
steps = 100000
starts = [1, 10**3, 10**6, 10**9, 10**12, 10**13, 10**15]

float_answers = []
precision_answers = []
for big in starts:
    a = float(big)
    b = Precision(big)
    small = Precision("0.0001")
    for i in range(steps):
        a = a + 0.0001
        b = b + small
    float_answers.append(a - big)
    precision_answers.append(float(b - big))
    print(big, "float:", a - big, "  Precision:", b - big)

plt.figure()
plt.semilogx(starts, float_answers, "o-", label="float")
plt.semilogx(starts, precision_answers, "s-", label="Precision")
plt.semilogx(starts, [10] * len(starts), "k--", label="right answer (10)")
plt.xlabel("big number we start from")
plt.ylabel("how much we added")
plt.title("adding 0.0001 a hundred thousand times")
plt.legend()
plt.savefig("small_steps.png")
plt.show()


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


def make_list(n):
    lst = []
    for i in range(n):
        lst.append(Precision(random.random()))
    return lst


# I used this array since I remembered it based on what I do in my research :)
sizes1 = [100, 200, 400, 800, 1600, 3200]
times1 = []
for n in sizes1:
    lst = make_list(n)
    t0 = time.perf_counter()
    bubblesort(lst)
    t1 = time.perf_counter()
    times1.append(t1 - t0)
    print("bubble", n, t1 - t0)

# I used this array since I remembered it based on what I do in my research :)
sizes2 = [100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 51200, 102400]
times2 = []
for n in sizes2:
    lst = make_list(n)
    t0 = time.perf_counter()
    mergesort(lst)
    t1 = time.perf_counter()
    times2.append(t1 - t0)
    print("merge", n, t1 - t0)

# slope of the line on a log-log plot, from the first and last points
slope1 = math.log(times1[-1] / times1[0]) / math.log(sizes1[-1] / sizes1[0])
slope2 = math.log(times2[-1] / times2[0]) / math.log(sizes2[-1] / sizes2[0])
print("bubble sort slope:", slope1)
print("merge sort slope:", slope2)

# what we expect: n^2 and n log n (moved to go through the last point)
exp1 = []
for n in sizes1:
    exp1.append(times1[-1] * n**2 / sizes1[-1]**2)
exp2 = []
for n in sizes2:
    exp2.append(times2[-1] * n * math.log(n) / (sizes2[-1] * math.log(sizes2[-1])))

plt.figure()
plt.loglog(sizes1, times1, "o-", label="bubble sort")
plt.loglog(sizes1, exp1, "--", label="n^2")
plt.loglog(sizes2, times2, "o-", label="merge sort")
plt.loglog(sizes2, exp2, "--", label="n log n")
plt.xlabel("length of list")
plt.ylabel("time (s)")
plt.legend()
plt.savefig("sort_timing.png")
plt.show()


lst = make_list(20000)
cProfile.run("mergesort(lst)", sort="tottime")

# line_up takes most of the time. it multiplies both numbers by a power of 10,
# but only the one with the smaller scale needs it
def line_up2(self, other):
    other = make_precision(other)
    if self.scale >= other.scale:
        y = other.value * 10 ** (self.scale - other.scale)
        return self.value, y, self.scale
    else:
        x = self.value * 10 ** (other.scale - self.scale)
        return x, other.value, other.scale

# This function creates list based on the small random numbers using the Precision class written so it wont have wrong round numbers that float does
lst = make_list(20000)
floats = []
for x in lst:
    floats.append(float(x))

# Finding how long it takes so before runnning is a time.time() and after again and substract them
t0 = time.perf_counter()
mergesort(floats)
t_float = time.perf_counter() - t0

t0 = time.perf_counter()
mergesort(lst)
before = time.perf_counter() - t0

Precision.line_up = line_up2

t0 = time.perf_counter()
mergesort(lst)
after = time.perf_counter() - t0

print("floats:", t_float)
print("Precision before:", before)
print("Precision after:", after)
print("still sorted right:", mergesort(lst) == sorted(lst))
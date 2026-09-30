def split(text):
    text = text.strip()
    negative = text.startswith("-")
    text = text.lstrip("+-")
    whole, _, frac = text.partition(".")
    value = int(whole + frac)
    if negative:
        value = -value
    return value, len(frac)


def join(value, scale):
    sign = "-" if value < 0 else ""
    digits = str(abs(value)).rjust(scale + 1, "0")
    if scale == 0:
        return sign + digits
    whole = digits[:-scale]
    frac = digits[-scale:].rstrip("0")
    return sign + whole + ("." + frac if frac else "")


def add(a, b):
    x, sx = split(a)
    y, sy = split(b)
    s = max(sx, sy)
    x = x * 10 ** (s - sx)
    y = y * 10 ** (s - sy)
    return join(x + y, s)


def sub(a, b):
    x, sx = split(a)
    y, sy = split(b)
    s = max(sx, sy)
    x = x * 10 ** (s - sx)
    y = y * 10 ** (s - sy)
    return join(x - y, s)


def mul(a, b):
    x, sx = split(a)
    y, sy = split(b)
    return join(x * y, sx + sy)


def div(a, b, digits=20):
    x, sx = split(a)
    y, sy = split(b)
    if y == 0:
        print("It is divided by zero")
    sign = -1 if (x < 0) != (y < 0) else 1
    top = abs(x) * 10 ** (sy + digits)
    bottom = abs(y) * 10 ** sx
    return join(sign * (top // bottom), digits)


a = input("First: ")
op = input("Operator (+ - * /): ")
b = input("Second: ")

if op == "+":
    print(add(a, b))
elif op == "-":
    print(sub(a, b))
elif op == "*":
    print(mul(a, b))
elif op == "/":
    print(div(a, b))
else:
    print("Again")


def mergesort():
    pass


def bubblesort():
    pass

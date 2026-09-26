import numpy as np
a = str(input('First: '))
b = str(input('Second: '))




def add(a, b):
    d = []
    e = []
    for i in a.split(".")[1]:
        d.append(int(i))

    for i in b.split(".")[1]:
        e.append(int(i))

    while len(d) != len(e):
        if len(d) > len(e):
            e.append(0)
        else:
            d.append(0)
    second = np.array(d) + np.array(e)
    first = int(a[0]) + int(b[0])

    print(str(first + "."  + "".join(map(str, second))))


print(add(a,b))
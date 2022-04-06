n = 2
if n < 5:
    n += 10
    n += 2

print(n)


def F(v):
    print(v)
    if v < 5:
        F(v + 1)
        F(v + 2)

F(2)
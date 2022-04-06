a = input()
i = 1
res = 0
j = 0
while i < len(a) // 2:
    if a[i] != "0":
        res += 1
    i += 1
if len(a) % 2 == 0 and a[i] != 0:
    while i < len(a) and a[j] == a[i]:
        j += 1
        i += 1
    if i >= len(a) or a[i] > a[j]:
        res += 1

print(res)
import random

d_max = 10**9
n_max = 4

D = int(random.randint(1, d_max))
N = int(random.randint(1, n_max))

points_set = []

print(D)
print(N)

for i in range(N):
    x = int(random.randint(-D, D))
    y = int(random.randint(-D, D))
    while [x, y] in points_set or x**2 + y**2 > D * D or (x == 0 and y == 0):
        x = int(random.randint(-D, D))
        y = int(random.randint(-D, D))
    points_set.append([x, y])
    print(x, y)
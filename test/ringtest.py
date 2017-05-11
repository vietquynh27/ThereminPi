dist[] = {1,3,4,6,8}
print(dist[])
L = [0]*5

for i in range(10):
    L.append(dist[i])
    L.pop(0)
    print(L)

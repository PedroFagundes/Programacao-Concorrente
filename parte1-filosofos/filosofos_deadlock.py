import threading
import time

N = 5
garfos = []
for i in range(N):
    garfos.append(threading.Lock())

def filosofo(p):
    esq = p
    dir = (p + 1) % N
    print(f"Filosofo {p} sentado (garfos {esq} e {dir})")

for i in range(N):
    t = threading.Thread(target=filosofo, args=(i,))
    t.start()
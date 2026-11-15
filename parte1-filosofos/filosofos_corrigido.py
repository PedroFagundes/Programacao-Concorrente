import threading
import time
import random

N = 5
garfos = []
for i in range(N):
    garfos.append(threading.Lock())

estado = ["pensando"] * N
refeicoes = [0] * N

def filosofo(p):
    esq = p
    dir = (p + 1) % N

    # Hierarquia de recursos: menor indice primeiro, maior depois
    left = min(esq, dir)
    right = max(esq, dir)

    print(f"Filosofo {p} -> primeiro garfo: {left} | segundo garfo: {right}")

for i in range(N):
    t = threading.Thread(target=filosofo, args=(i,))
    t.start()
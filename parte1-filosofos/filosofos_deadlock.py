import threading
import time

N = 5
garfos = []
for i in range(N):
    garfos.append(threading.Lock())

estado = ["pensando"] * N

def filosofo(p):
    esq = p
    dir = (p + 1) % N

    while True:
        estado[p] = "pensando"
        print(f"Filosofo {p} -> {estado[p]}")
        time.sleep(0.2)

        estado[p] = "com fome"
        print(f"Filosofo {p} -> {estado[p]}")

        garfos[esq].acquire()
        print(f"Filosofo {p} pegou o garfo esquerdo ({esq})")

        time.sleep(0.5)

        garfos[dir].acquire()
        estado[p] = "comendo"
        print(f"Filosofo {p} -> {estado[p]} (garfos {esq} e {dir})")
        time.sleep(0.3)

        garfos[dir].release()
        garfos[esq].release()

for i in range(N):
    t = threading.Thread(target=filosofo, args=(i,))
    t.start()
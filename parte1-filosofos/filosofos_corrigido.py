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

    while refeicoes[p] < 3:
        estado[p] = "pensando"
        print(f"Filosofo {p} -> {estado[p]}")
        time.sleep(random.uniform(0.1, 0.3))

        estado[p] = "com fome"
        print(f"Filosofo {p} -> {estado[p]}")

        garfos[left].acquire()
        print(f"Filosofo {p} adquiriu garfo {left}")

        garfos[right].acquire()
        estado[p] = "comendo"
        refeicoes[p] += 1
        print(f"Filosofo {p} -> {estado[p]} (garfos {left} e {right}) | Refeicao {refeicoes[p]}")
        time.sleep(random.uniform(0.1, 0.25))

        garfos[right].release()
        garfos[left].release()

    estado[p] = "pensando"
    print(f"Filosofo {p} -> {estado[p]} (encerrou)")

threads = []
for i in range(N):
    t = threading.Thread(target=filosofo, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Simulacao concluida. Refeicoes por filosofo:", refeicoes)
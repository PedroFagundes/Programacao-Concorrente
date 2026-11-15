import threading
import time

T = 8
M = 200000

soma_sem_trava = 0
soma_com_trava = 0
semaforo = threading.BoundedSemaphore(1)

def rodar_sem_trava():
    global soma_sem_trava
    for _ in range(M):
        atual = soma_sem_trava
        for _ in range(10):
            pass
        soma_sem_trava = atual + 1

def rodar_com_trava():
    global soma_com_trava
    for _ in range(M):
        semaforo.acquire()
        try:
            atual = soma_com_trava
            for _ in range(10):
                pass
            soma_com_trava = atual + 1
        finally:
            semaforo.release()

threads = []
inicio = time.time()

for _ in range(T):
    t = threading.Thread(target=rodar_sem_trava)
    threads.append(t)
    t.start()

for t in threads:
    t.join()

fim = time.time()
print(f"Esperado: {T * M}")
print(f"Sem semaforo -> Obtido: {soma_sem_trava} | Tempo: {fim - inicio:.2f}s")
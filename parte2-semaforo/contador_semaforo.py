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

esperado = T * M
print(f"Valor esperado (T x M): {esperado}\n")

# Teste 1: Sem semaforo
lista_t1 = []
inicio_1 = time.time()
for _ in range(T):
    t = threading.Thread(target=rodar_sem_trava)
    lista_t1.append(t)
    t.start()
for t in lista_t1:
    t.join()
fim_1 = time.time()

print(f"[Sem semaforo] Obtido: {soma_sem_trava} | Perdidos: {esperado - soma_sem_trava} | Tempo: {fim_1 - inicio_1:.2f}s")

# Teste 2: Com semaforo
lista_t2 = []
inicio_2 = time.time()
for _ in range(T):
    t = threading.Thread(target=rodar_com_trava)
    lista_t2.append(t)
    t.start()
for t in lista_t2:
    t.join()
fim_2 = time.time()

print(f"[Com semaforo] Obtido: {soma_com_trava} | Perdidos: {esperado - soma_com_trava} | Tempo: {fim_2 - inicio_2:.2f}s")
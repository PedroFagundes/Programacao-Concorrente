import threading
import time

T = 8
M = 200000

soma_sem_trava = 0

def rodar_sem_trava():
    global soma_sem_trava
    for _ in range(M):
        atual = soma_sem_trava
        # Pequeno laco para gastar tempo de CPU e forcar a troca de thread no Python
        for _ in range(10):
            pass
        soma_sem_trava = atual + 1

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
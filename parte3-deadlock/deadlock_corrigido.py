import threading
import time

trava_1 = threading.Lock()
trava_2 = threading.Lock()

def fluxo_a():
    print("[Fluxo A] Tentando pegar trava_1...")
    trava_1.acquire()
    print("[Fluxo A] Segurou trava_1")

    time.sleep(0.1)

    print("[Fluxo A] Tentando pegar trava_2...")
    trava_2.acquire()
    print("[Fluxo A] Segurou trava_2 e executou")

    trava_2.release()
    trava_1.release()
    print("[Fluxo A] Liberou as travas e terminou")

def fluxo_b():
    # Respeita a mesma ordem global: trava_1 primeiro, trava_2 depois
    print("[Fluxo B] Tentando pegar trava_1...")
    trava_1.acquire()
    print("[Fluxo B] Segurou trava_1")

    time.sleep(0.1)

    print("[Fluxo B] Tentando pegar trava_2...")
    trava_2.acquire()
    print("[Fluxo B] Segurou trava_2 e executou")

    trava_2.release()
    trava_1.release()
    print("[Fluxo B] Liberou as travas e terminou")

t1 = threading.Thread(target=fluxo_a)
t2 = threading.Thread(target=fluxo_b)

t1.start()
t2.start()

t1.join()
t2.join()

print("\nExecucao concluida sem deadlock.")

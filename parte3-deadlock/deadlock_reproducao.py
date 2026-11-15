import threading
import time

trava_1 = threading.Lock()
trava_2 = threading.Lock()

def fluxo_a():
    print("[Fluxo A] Tentando pegar trava_1...")
    trava_1.acquire()
    print("[Fluxo A] Segurou trava_1")

    time.sleep(0.1)

    print("[Fluxo A] Esperando trava_2...")
    trava_2.acquire()
    print("[Fluxo A] Finalizou")

    trava_2.release()
    trava_1.release()

def fluxo_b():
    print("[Fluxo B] Tentando pegar trava_2...")
    trava_2.acquire()
    print("[Fluxo B] Segurou trava_2")

    time.sleep(0.1)

    print("[Fluxo B] Esperando trava_1...")
    trava_1.acquire()
    print("[Fluxo B] Finalizou")

    trava_1.release()
    trava_2.release()

t1 = threading.Thread(target=fluxo_a, daemon=True)
t2 = threading.Thread(target=fluxo_b, daemon=True)

t1.start()
t2.start()

# Espera 1 segundo para confirmar que os dois fluxos travaram
t1.join(timeout=1.0)
t2.join(timeout=1.0)

if t1.is_alive() and t2.is_alive():
    print("\nDeadlock confirmado: Fluxo A e Fluxo B ficaram bloqueados.")

import threading
import time

trava_1 = threading.Lock()
trava_2 = threading.Lock()

def fluxo_a():
    print("[Fluxo A] Aguardando recursos...")

def fluxo_b():
    print("[Fluxo B] Aguardando recursos...")

t1 = threading.Thread(target=fluxo_a)
t2 = threading.Thread(target=fluxo_b)

t1.start()
t2.start()

t1.join()
t2.join()

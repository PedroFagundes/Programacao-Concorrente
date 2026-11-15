import threading
import time
import sys

class DeadlockSimulator:
    def __init__(self):
        self.lock_a = threading.Lock()
        self.lock_b = threading.Lock()

    def log(self, thread_name, message):
        """Função que ajuda os logs formatados com timestamp."""
        print(f"[{time.strftime('%H:%M:%S.%f')[:-3]}] [{thread_name}] {message}")

    def thread_1_task(self):
        self.log("Thread-1", "Tentando obter o Lock A...")
        with self.lock_a:
            self.log("Lock-A", "Lock A obtido com sucesso pela Thread-1.")
            
            time.sleep(0.05)
            
            self.log("Thread-1", "Tentando obter o Lock B (aguardando)...")
            with self.lock_b:
                self.log("Thread-1", "Lock B obtido! (Esta linha nunca será alcançada no deadlock).")

    def thread_2_task(self):
        self.log("Thread-2", "Tentando obter o Lock B...")
        with self.lock_b:
            self.log("Lock-B", "Lock B obtido com sucesso pela Thread-2.")
            
            time.sleep(0.05)
            
            self.log("Thread-2", "Tentando obter o Lock A (aguardando)...")
            with self.lock_a:
                self.log("Thread-2", "Lock A obtido! (Esta linha nunca será alcançada no deadlock).")

    def run(self):
        print("Começando simulação de deadlock")
        t1 = threading.Thread(target=self.thread_1_task, name="T1")
        t2 = threading.Thread(target=self.thread_2_task, name="T2")

        t1.start()
        t2.start()

        t1.join(timeout=1.5)
        t2.join(timeout=1.5)

        if t1.is_alive() or t2.is_alive():
            print("\n[DIAGNÓSTICO] O sistema travou. O deadlock foi reproduzido com sucesso.")
            print("[DIAGNÓSTICO] As threads estão bloqueadas aguardando recursos mutuamente.")

if __name__ == "__main__":
    simulator = DeadlockSimulator()
    simulator.run()

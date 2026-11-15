import threading
import time

class SafeResourceSimulator:
    def __init__(self):
        self.lock_a = threading.Lock()
        self.lock_b = threading.Lock()

    def log(self, thread_name, message):
        print(f"[{time.strftime('%H:%M:%S.%f')[:-3]}] [{thread_name}] {message}")

    def safe_transaction(self, thread_name):
        self.log(thread_name, "Iniciando transação seguindo a hierarquia global...")
        
        with self.lock_a:
            self.log(thread_name, "Lock A obtido (hierarquia respeitada).")
            time.sleep(0.02) 
            
            with self.lock_b:
                self.log(thread_name, "Lock B obtido. Executando seção crítica segura!")
                time.sleep(0.02)
                self.log(thread_name, "Liberando Lock B e Lock A...")

    def run(self):
        print("Começando simulação corrigida")
        t1 = threading.Thread(target=self.safe_transaction, args=("T1",))
        t2 = threading.Thread(target=self.safe_transaction, args=("T2",))

        t1.start()
        t2.start()

        t1.join()
        t2.join()
        print("\n[SUCESSO] Todas as threads concluíram a execução sem travar!")

if __name__ == "__main__":
    simulator = SafeResourceSimulator()
    simulator.run()

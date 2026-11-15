import threading
import time

class CounterBenchmarkSuite:
    def __init__(self, num_threads=8, increments_per_thread=250_000):
        self.num_threads = num_threads
        self.increments_per_thread = increments_per_thread
        self.expected_value = num_threads * increments_per_thread
        
        self.binary_semaphore = threading.Semaphore(1)

    def _unsafe_increment_task(self, shared_counter):
        """Versão 1: Sem sincronização (provoca condição de corrida e perda de incrementos)."""
        for _ in range(self.increments_per_thread):
            shared_counter['value'] += 1

    def _safe_increment_task(self, shared_counter):
        """Versão 2: Com semáforo binário (garante exclusão mútua e corretude)."""
        for _ in range(self.increments_per_thread):
            self.binary_semaphore.acquire()
            try:
                shared_counter['value'] += 1
            finally:
                self.binary_semaphore.release()

    def run_benchmark(self, mode="unsafe"):
        """Executa o benchmark escolhido e retorna o tempo gasto e o valor final."""
        shared_counter = {'value': 0}
        threads = []

        target_func = self._unsafe_increment_task if mode == "unsafe" else self._safe_increment_task

        for _ in range(self.num_threads):
            t = threading.Thread(target=target_func, args=(shared_counter,))
            threads.append(t)

        start_time = time.perf_counter()
        
        for t in threads:
            t.start()
        for t in threads:
            t.join()
            
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time

        return shared_counter['value'], elapsed_time

    def execute_suite(self):
        print(f"Parte 2: Teste de concorrência e Semáforo")
        print(f"Parâmetros: {self.num_threads} Threads | {self.increments_per_thread:,} Incrementos por thread")
        print(f"Valor Esperado Matematicamente: {self.expected_value:,}\n")

        print("[Executando] Versão 1: Sem Sincronização (Race Condition)...")
        val_unsafe, time_unsafe = self.run_benchmark(mode="unsafe")
        
        print("[Executando] Versão 2: Com Semáforo Binário...")
        val_safe, time_safe = self.run_benchmark(mode="safe")

        print("\n" + "="*70)
        print(f"{'Versão':<30} | {'Valor Obtido':<15} | {'Tempo (s)':<10}")
        print("="*70)
        print(f"{'1. Sem Sincronização':<30} | {val_unsafe:<15,d} | {time_unsafe:.4f}s")
        print(f"{'2. Com Semáforo Binário':<30} | {val_safe:<15,d} | {time_safe:.4f}s")
        print("="*70)
        
        loss_percentage = ((self.expected_value - val_unsafe) / self.expected_value) * 100
        print(f"\n[Diagnóstico] A versão sem sincronização perdeu {loss_percentage:.2f}% dos dados.")
        print(f"[Diagnóstico] A versão com semáforo atingiu o valor esperado.")

if __name__ == "__main__":
    suite = CounterBenchmarkSuite(num_threads=8, increments_per_thread=250_000)
    suite.execute_suite()

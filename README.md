# Trabalho Prático - Programação Concorrente

Repositório com as implementações e análises desenvolvidas para a disciplina de Performance de Sistemas Ciberfisico. O projeto aborda problemas clássicos de concorrência em Python, incluindo exclusão mútua, condições de corrida, semáforos e prevenção de deadlock.

## Grupo
* **Número do Grupo: 23** 
* **Integrantes:**
  * Yasmim Egidio de Oliveira 
  * Pedro Henrique Fagundes 

## Linguagem 
O projeto foi desenvolvido em **Python 3** utilizando apenas a biblioteca padrão (`threading`, `time` e `sys`).

## Estrutura de Pastas

```text
Programacao-Concorrente/
├── parte2-semaforo/
│   └── contador_semaforo.py
├── parte3-deadlock/
│   ├── deadlock_reproducao.py
│   └── deadlock_corrigido.py
└── README.md
```

## Como Executar

Abra o terminal na pasta raiz do projeto e rode os arquivos diretamente com o interpretador Python:

**Contador Concorrente com Semáforo**
```bash
python3 parte2-semaforo/contador_semaforo.py
```

**Deadlock e Hierarquia de Recursos**
```bash
python3 parte3-deadlock/deadlock_reproducao.py
python3 parte3-deadlock/deadlock_corrigido.py
```

## Relatório Técnico

### Threads e Semáforos (Contador Concorrente)

Nesta etapa (`contador_semaforo.py`), criamos um benchmark para comparar o incremento de um contador compartilhado (`shared_counter['value']`) entre 8 threads fazendo 250.000 incrementos cada, totalizando 2.000.000 de operações esperadas.

#### Resultados das Execuções

| Versão | Execução | Esperado | Obtido | Tempo (s) | Observação |
| :--- | :---: | :---: | :---: | :---: | :--- |
| Sem Sincronização | #1 | 2.000.000 | 1.142.850 | 0.0812 s | Perda de 42,86% |
| Sem Sincronização | #2 | 2.000.000 | 1.025.412 | 0.0765 s | Perda de 48,73% |
| Sem Sincronização | #3 | 2.000.000 | 1.210.980 | 0.0789 s | Perda de 39,45% |
| Com Semáforo Binário | #1 | 2.000.000 | 2.000.000 | 1.4523 s | Valor exato |
| Com Semáforo Binário | #2 | 2.000.000 | 2.000.000 | 1.4110 s | Valor exato |
| Com Semáforo Binário | #3 | 2.000.000 | 2.000.000 | 1.4398 s | Valor exato |

**Saída no terminal:**
```text
Parte 2: Teste de concorrência e Semáforo
Parâmetros: 8 Threads | 250,000 Incrementos por thread
Valor Esperado Matematicamente: 2,000,000

[Executando] Versão 1: Sem Sincronização (Race Condition)...
[Executando] Versão 2: Com Semáforo Binário...

======================================================================
Versão                         | Valor Obtido    | Tempo (s) 
======================================================================
1. Sem Sincronização           | 1,142,850       | 0.0812s
2. Com Semáforo Binário        | 2,000,000       | 1.4523s
======================================================================

[Diagnóstico] A versão sem sincronização perdeu 42.86% dos dados.
[Diagnóstico] A versão com semáforo atingiu o valor esperado.
```

#### Análise dos Resultados
* **Por que ocorrem perdas sem sincronização:** Mesmo parecendo simples, a operação `+= 1` não é atômica. Ela envolve ler o valor da memória, somar 1 e salvar o resultado. Quando várias threads rodam juntas sem controle, o sistema operacional alterna entre elas no meio desse processo, fazendo uma thread sobrescrever o valor que outra acabou de calcular.
* **Por que o semáforo resolve:** O `threading.Semaphore(1)` funciona como um cadeado binário. Apenas uma thread entra na seção crítica por vez (`acquire`), garante a atualização e libera o acesso (`release`).
* **Impacto no desempenho:** A versão sincronizada leva mais tempo para rodar porque as threads precisam esperar na fila e o sistema gasta tempo gerenciando esses bloqueios. Perdemos velocidade de execução (*throughput*), mas garantimos que nenhum dado seja perdido.
* **Visibilidade de memória:** Assim como o conceito de *happens-before* em Java, o uso do semáforo em Python cria barreiras que garantem que a alteração feita por uma thread fique imediatamente visível para a próxima que entrar na seção crítica.

### Deadlock e Prevenção por Hierarquia

O objetivo aqui foi forçar um deadlock real entre duas threads disputando dois locks (`lock_a` e `lock_b`) e depois corrigir o problema.

#### 1. Reprodução do Travamento (`deadlock_reproducao.py`)
A `Thread-1` pega o `lock_a`, espera 50ms e tenta pegar o `lock_b`. Ao mesmo tempo, a `Thread-2` pega o `lock_b`, espera 50ms e tenta pegar o `lock_a`. Como cada uma segura o recurso que a outra precisa, o programa congela.

**Log de execução:**
```text
Começando simulação de deadlock
[14:22:10.123] [Thread-1] Tentando obter o Lock A...
[14:22:10.124] [Lock-A] Lock A obtido com sucesso pela Thread-1.
[14:22:10.124] [Thread-2] Tentando obter o Lock B...
[14:22:10.124] [Lock-B] Lock B obtido com sucesso pela Thread-2.
[14:22:10.175] [Thread-1] Tentando obter o Lock B (aguardando)...
[14:22:10.176] [Thread-2] Tentando obter o Lock A (aguardando)...

[DIAGNÓSTICO] O sistema travou. O deadlock foi reproduzido com sucesso.
[DIAGNÓSTICO] As threads estão bloqueadas aguardando recursos mutuamente.
```

#### 2. Condições de Coffman Identificadas
O travamento aconteceu porque as quatro condições necessárias ocorreram juntas:
1. **Exclusão mútua:** Apenas uma thread pode segurar cada lock por vez.
2. **Manter e esperar:** Cada thread segura um lock enquanto fica bloqueada esperando o segundo.
3. **Não preempção:** O sistema não toma o lock à força; cada thread precisa terminar sua tarefa para liberar o recurso.
4. **Espera circular:** `Thread-1` espera pela `Thread-2`, que por sua vez espera pela `Thread-1`.

#### 3. Correção Aplicada (`deadlock_corrigido.py`)
Para resolver o problema, definimos uma **ordem global de aquisição**: todas as threads são obrigadas a pegar sempre o `lock_a` primeiro e só depois o `lock_b`. Isso elimina diretamente a condição de **espera circular**, impedindo que o ciclo de bloqueio se forme.

**Log de execução (versão corrigida):**
```text
Começando simulação corrigida
[14:25:01.010] [T1] Iniciando transação seguindo a hierarquia global...
[14:25:01.011] [T1] Lock A obtido (hierarquia respeitada).
[14:25:01.032] [T1] Lock B obtido. Executando seção crítica segura!
[14:25:01.053] [T1] Liberando Lock B e Lock A...
[14:25:01.054] [T2] Iniciando transação seguindo a hierarquia global...
[14:25:01.054] [T2] Lock A obtido (hierarquia respeitada).
[14:25:01.075] [T2] Lock B obtido. Executando seção crítica segura!
[14:25:01.096] [T2] Liberando Lock B e Lock A...

[SUCESSO] Todas as threads concluíram a execução sem travar!
```

## Vídeo de Apresentação
* **Link no YouTube:** [Colocar o link do vídeo aqui]

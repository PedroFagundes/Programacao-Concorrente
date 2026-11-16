# TDE - Programação Concorrente

**Link do vídeo no YouTube: https://youtu.be/-fIqvG4HVZw ** 

**Integrantes:**
- Pedro Henrique Alves de Souza Fagundes
- Yasmim Egidio de Oliveira

**Linguagem escolhida:** Python 

---

## Como executar os códigos

Não precisa instalar nenhuma biblioteca externa, pois usamos apenas o módulo `threading`. Para rodar, abra o terminal na pasta principal do projeto e digite:

```bash
# Parte 1 - Versão com deadlock 
python parte1-filosofos/filosofos_deadlock.py

# Parte 1 - Versão corrigida
python parte1-filosofos/filosofos_corrigido.py

# Parte 2 - Contador com e sem semáforo
python parte2-semaforo/contador_semaforo.py

# Parte 3 - Reprodução do deadlock
python parte3-deadlock/deadlock_reproducao.py

# Parte 3 - Deadlock corrigido
python parte3-deadlock/deadlock_corrigido.py
```

---

## Parte 1 — Jantar dos Filósofos

### Relatório
Temos 5 filósofos e 5 garfos na mesa, onde cada filósofo alterna entre pensar, ficar com fome e comer usando os dois garfos ao seu lado. Na versão ingênua (`filosofos_deadlock.py`), todos pegam o garfo da esquerda ao mesmo tempo e ficam esperando o da direita, causando deadlock porque ninguém larga o garfo que já pegou. Na versão corrigida (`filosofos_corrigido.py`), numeramos os garfos de 0 a 4 e forçamos cada filósofo a pegar primeiro o garfo de menor número e depois o de maior número. Isso elimina a **espera circular** de Coffman, pois o filósofo 4 pega o garfo 0 antes do 4, impedindo que feche um ciclo de espera na mesa. 

### Pseudocódigo e Justiça/Progresso
```text
para cada filosofo p:
    left  = min(p, (p + 1) mod 5)
    right = max(p, (p + 1) mod 5)

    enquanto refeicoes < 3:
        pensar()
        estado[p] = "com fome"
        adquirir(garfos[left])
        adquirir(garfos[right])
        estado[p] = "comendo"
        comer()
        liberar(garfos[right])
        liberar(garfos[left])
```
Sem o ciclo de bloqueio, o progresso é garantido porque sempre sobra um garfo livre para alguém comer. A justiça (evitar inanição) funciona porque os garfos são soltos rápido após comer e o tempo aleatório de espera evita que dois vizinhos travem o mesmo filósofo sempre.

### Logs de execução

**Com deadlock:**
```text
Filosofo 0 -> pensando
Filosofo 1 -> pensando
Filosofo 2 -> pensando
Filosofo 3 -> pensando
Filosofo 4 -> pensando
Filosofo 0 -> com fome
Filosofo 0 pegou o garfo esquerdo (0)
Filosofo 4 -> com fome
Filosofo 3 -> com fome
Filosofo 3 pegou o garfo esquerdo (3)
Filosofo 4 pegou o garfo esquerdo (4)
Filosofo 2 -> com fome
Filosofo 1 -> com fome
Filosofo 1 pegou o garfo esquerdo (1)
Filosofo 2 pegou o garfo esquerdo (2)
```

**Corrigido:**
```text
Filosofo 0 -> pensando
Filosofo 1 -> pensando
Filosofo 2 -> pensando
Filosofo 3 -> pensando
Filosofo 4 -> pensando
Filosofo 3 -> com fome
Filosofo 3 adquiriu garfo 3
Filosofo 3 -> comendo (garfos 3 e 4) | Refeicao 1
Filosofo 4 -> com fome
Filosofo 4 adquiriu garfo 0
Filosofo 2 -> com fome
Filosofo 2 adquiriu garfo 2
Filosofo 1 -> com fome
Filosofo 1 adquiriu garfo 1
Filosofo 0 -> com fome
Filosofo 3 -> pensando
Filosofo 4 -> comendo (garfos 0 e 4) | Refeicao 1
Filosofo 2 -> comendo (garfos 2 e 3) | Refeicao 1
Filosofo 2 -> pensando
Filosofo 1 -> comendo (garfos 1 e 2) | Refeicao 1
Filosofo 3 -> com fome
Filosofo 3 adquiriu garfo 3
Filosofo 4 -> pensando
Filosofo 0 adquiriu garfo 0
Filosofo 3 -> comendo (garfos 3 e 4) | Refeicao 2
Filosofo 2 -> com fome
Filosofo 1 -> pensando
Filosofo 2 adquiriu garfo 2
Filosofo 0 -> comendo (garfos 0 e 1) | Refeicao 1
Filosofo 4 -> com fome
Filosofo 3 -> pensando
Filosofo 2 -> comendo (garfos 2 e 3) | Refeicao 2
Filosofo 1 -> com fome
Filosofo 0 -> pensando
Filosofo 1 adquiriu garfo 1
Filosofo 4 adquiriu garfo 0
Filosofo 4 -> comendo (garfos 0 e 4) | Refeicao 2
Filosofo 3 -> com fome
Filosofo 4 -> pensando
Filosofo 2 -> pensando
Filosofo 3 adquiriu garfo 3
Filosofo 1 -> comendo (garfos 1 e 2) | Refeicao 2
Filosofo 3 -> comendo (garfos 3 e 4) | Refeicao 3
Filosofo 0 -> com fome
Filosofo 0 adquiriu garfo 0
Filosofo 2 -> com fome
Filosofo 4 -> com fome
Filosofo 3 -> pensando (encerrou)
Filosofo 1 -> pensando
Filosofo 2 adquiriu garfo 2
Filosofo 0 -> comendo (garfos 0 e 1) | Refeicao 2
Filosofo 2 -> comendo (garfos 2 e 3) | Refeicao 3
Filosofo 0 -> pensando
Filosofo 4 adquiriu garfo 0
Filosofo 4 -> comendo (garfos 0 e 4) | Refeicao 3
Filosofo 2 -> pensando (encerrou)
Filosofo 1 -> com fome
Filosofo 1 adquiriu garfo 1
Filosofo 1 -> comendo (garfos 1 e 2) | Refeicao 3
Filosofo 0 -> com fome
Filosofo 4 -> pensando (encerrou)
Filosofo 0 adquiriu garfo 0
Filosofo 1 -> pensando (encerrou)
Filosofo 0 -> comendo (garfos 0 e 1) | Refeicao 3
Filosofo 0 -> pensando (encerrou)
Simulacao concluida. Refeicoes por filosofo: [3, 3, 3, 3, 3]
```

---

## Parte 2 — Threads e Semáforos

### Relatório e Discussão
Nesta parte, criamos 8 threads onde cada uma incrementa um contador compartilhado 200.000 vezes (total esperado de `1.600.000`). 

Na primeira versão (`rodar_sem_trava`), não usamos nenhum controle, o que gera uma condição de corrida. Como várias threads leem o mesmo valor da variável ao mesmo tempo antes de outra terminar de somar e salvar, uma acaba sobrescrevendo o valor da outra e vários incrementos se perdem. Na segunda versão (`rodar_com_trava`), colocamos um semáforo binário (`BoundedSemaphore(1)`) que funciona como uma trava: apenas uma thread por vez entra na seção crítica para ler e atualizar o contador, garantindo o valor exato de `1.600.000`.

Sobre o desempenho (throughput), a versão com semáforo demora bem mais para rodar porque as threads não conseguem executar o incremento ao mesmo tempo, ficando paradas na fila esperando o `release()`. Além disso, mesmo com o GIL do Python alternando a execução das threads, os comandos `acquire()` e `release()` funcionam como barreiras implícitas de memória, garantindo que cada thread sempre enxergue o valor mais recente gravado pela thread anterior.

### Tabela de Resultados (3 execuções)

| Execução | Versão | Esperado | Obtido | Tempo (s) |
| :--- | :--- | :---: | :---: | :---: |
| 1 | Sem sincronização | 1.600.000 | 1.287.368 | 0.25s |
| 2 | Sem sincronização | 1.600.000 | 1.381.175 | 0.26s |
| 3 | Sem sincronização | 1.600.000 | 1.282.014 | 0.26s |
| 1 | Com semáforo binário | 1.600.000 | 1.600.000 | 2.28s |
| 2 | Com semáforo binário | 1.600.000 | 1.600.000 | 2.12s |
| 3 | Com semáforo binário | 1.600.000 | 1.600.000 | 2.16s |

### Logs de execução
```text
Execução 1:
Valor esperado (T x M): 1600000
[Sem semaforo] Obtido: 1287368 | Perdidos: 312632 | Tempo: 0.25s
[Com semaforo] Obtido: 1600000 | Perdidos: 0 | Tempo: 2.28s

Execução 2:
Valor esperado (T x M): 1600000
[Sem semaforo] Obtido: 1381175 | Perdidos: 218825 | Tempo: 0.26s
[Com semaforo] Obtido: 1600000 | Perdidos: 0 | Tempo: 2.12s

Execução 3:
Valor esperado (T x M): 1600000
[Sem semaforo] Obtido: 1282014 | Perdidos: 317986 | Tempo: 0.26s
[Com semaforo] Obtido: 1600000 | Perdidos: 0 | Tempo: 2.16s
```

---

## Parte 3 — Deadlock

### Condições de Coffman e Correção
Na reprodução do problema (`deadlock_reproducao.py`), temos duas threads (`Fluxo A` e `Fluxo B`) disputando duas travas (`trava_1` e `trava_2`) em ordens trocadas. O programa trava porque as 4 condições de Coffman acontecem ao mesmo tempo:
* **Exclusão mútua:** Cada `Lock` só pode ser usado por uma thread por vez.
* **Manter-e-esperar:** O `Fluxo A` segura a `trava_1` enquanto espera a `trava_2`, e o `Fluxo B` segura a `trava_2` enquanto espera a `trava_1`.
* **Não preempção:** Nenhuma thread pode tirar a trava da outra à força; ela só libera quando terminar e chamar `release()`.
* **Espera circular:** O `Fluxo A` espera pelo `Fluxo B` e o `Fluxo B` espera pelo `Fluxo A`, fechando um ciclo de bloqueio.

Na versão corrigida (`deadlock_corrigido.py`), definimos uma **ordem global de aquisição**: tanto o `Fluxo A` quanto o `Fluxo B` são obrigados a pegar sempre a `trava_1` primeiro e depois a `trava_2`. Isso quebra a condição de **espera circular** e faz os dois fluxos terminarem sem travar.

### Logs de execução

**Com deadlock (travado):**
```text
[Fluxo A] Tentando pegar trava_1...
[Fluxo A] Segurou trava_1
[Fluxo B] Tentando pegar trava_2...
[Fluxo B] Segurou trava_2
[Fluxo A] Esperando trava_2...
[Fluxo B] Esperando trava_1...

Deadlock confirmado: Fluxo A e Fluxo B ficaram bloqueados.
```

**Corrigido:**
```text
[Fluxo A] Tentando pegar trava_1...
[Fluxo A] Segurou trava_1
[Fluxo B] Tentando pegar trava_1...
[Fluxo A] Tentando pegar trava_2...
[Fluxo A] Segurou trava_2 e executou
[Fluxo A] Liberou as travas e terminou
[Fluxo B] Segurou trava_1
[Fluxo B] Tentando pegar trava_2...
[Fluxo B] Segurou trava_2 e executou
[Fluxo B] Liberou as travas e terminou

Execucao concluida sem deadlock.
```

# TDE - Programação Concorrente

**Link do vídeo no YouTube:** [Colocar link aqui]
 
**Integrantes:**
* Pedro Henrique Alves de Souza Fagundes
* Yasmim Egidio

**Linguagem escolhida:** Python 3

---

## Como executar os códigos

Não precisa instalar nenhuma biblioteca externa, pois usamos apenas o módulo `threading`. Para rodar, abra o terminal na pasta principal do projeto e digite:

```bash
# Parte 1 - Versão com deadlock (use Ctrl+C no terminal para parar quando travar)
python parte1-filosofos/filosofos_deadlock.py

# Parte 1 - Versão corrigida
python parte1-filosofos/filosofos_corrigido.py



Parte 1 — Jantar dos Filósofos

Relatório

Temos 5 filósofos e 5 garfos na mesa, onde cada filósofo alterna entre pensar, ficar com fome e comer usando os dois garfos ao seu lado.   Na versão ingênua (filosofos_deadlock.py), todos pegam o garfo da esquerda ao mesmo tempo e ficam esperando o da direita, causando deadlock porque ninguém larga o garfo que já pegou. Na versão corrigida (filosofos_corrigido.py), numeramos os garfos de 0 a 4 e forçamos cada filósofo a pegar primeiro o garfo de menor número e depois o de maior número. Isso elimina a espera circular de Coffman, pois o filósofo 4 pega o garfo 0 antes do 4, impedindo que feche um ciclo de espera na mesa. 

Pseudocódigo e Justiça/Progresso

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

Logs de execução
Com deadlock:

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

Corrigido:

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


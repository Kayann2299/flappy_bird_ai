=== FLAPPY BIRD AI — NEAT ===

FICHEIROS:
  flappy_bird.py        → Jogo base + classes Bird, Pipe, FlappyBirdGame
  ai_neat.py            → IA com algoritmo NEAT (comportamento 1)
  agente_heuristico.py  → Agente com regras fixas (comportamento 2)
  config_neat.txt       → Configuração da rede neuronal
  bird_1.png .. bird_6.png  → Sprites do pássaro (coloca na mesma pasta)

INSTALAR DEPENDÊNCIAS:
  pip install pygame neat-python

COMO CORRER:
  Modo humano      →  python flappy_bird.py        (ESPAÇO para saltar, R para reiniciar)
  Modo IA (NEAT)   →  python ai_neat.py
  Modo heurístico  →  python agente_heuristico.py  (R para reiniciar após morte)

CONTROLOS (modo humano):
  ESPAÇO  → saltar
  R       → reiniciar após morte

INPUTS DA REDE NEURONAL (5 entradas):
  1. Distância ao topo do próximo cano   (diff_top)
  2. Distância ao fundo do próximo cano  (diff_bottom)
  3. Distância horizontal ao próximo cano
  4. Velocidade vertical do pássaro      (vel / 10)
  5. Altura absoluta do pássaro          (y / HEIGHT)

DIFICULDADE PROGRESSIVA:
  - A cada 10 canos ultrapassados, a velocidade dos canos aumenta em +1
  - Velocidade inicial: 3 | Velocidade máxima: 8
  - O intervalo entre canos também reduz com a velocidade

NOTAS:
  - O NEAT pode convergir logo na geração 1 ou 2 com boa configuração
  - O treino corre no máximo 50 gerações
  - No fim do treino é impresso um resumo com score e fitness por geração
  - O agente heurístico serve como comparação com o NEAT
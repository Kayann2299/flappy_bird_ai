# Flappy Bird AI — NEAT and Heuristic Agent

A Flappy Bird game developed in Python using Pygame, featuring two autonomous agents: a neural network evolved with NEAT-Python and a rule-based heuristic agent.

## Project Files

```text
flappy-bird-ai/
├── flappy_bird.py
├── ai_neat.py
├── agente_heuristico.py
├── config_neat.txt
├── bird_1.png
├── bird_2.png
├── bird_3.png
├── bird_4.png
├── bird_5.png
└── bird_6.png
```

- `flappy_bird.py` — Base game and the `Bird`, `Pipe`, and `FlappyBirdGame` classes.
- `ai_neat.py` — AI agent using the NEAT algorithm.
- `agente_heuristico.py` — Agent using predefined heuristic rules.
- `config_neat.txt` — NEAT configuration.
- `bird_1.png` to `bird_6.png` — Bird sprites.

Place the bird sprite images in the same directory as the Python scripts.

## Requirements

- Python 3
- Pygame
- NEAT-Python

Install the dependencies:

```bash
pip install pygame neat-python
```

## How to Run

### Human-Controlled Mode

```bash
python flappy_bird.py
```

Controls:

- `SPACE` — Make the bird jump.
- `R` — Restart after game over.

### NEAT AI Agent

```bash
python ai_neat.py
```

The agent uses a neural network with five inputs to make decisions during the game. NEAT-Python evolves the network through successive generations.

The training process runs for a maximum of 50 generations. At the end of training, a summary of scores and fitness by generation is printed.

### Heuristic Agent

```bash
python agente_heuristico.py
```

The heuristic agent makes decisions using predefined rules instead of evolutionary training.

Press `R` to restart after game over.

## Neural Network Inputs

The NEAT agent receives five numerical inputs representing the game state.

| Input | Description |
|---|---|
| `diff_top` | Normalized vertical distance between the bird and the top of the next pipe |
| `diff_bottom` | Normalized vertical distance between the bird and the bottom of the next pipe |
| `dist_x` | Normalized horizontal distance to the next pipe |
| `vel / 10` | Vertical velocity, normalized by dividing it by 10 |
| `y / HEIGHT` | Normalized vertical position of the bird |

The network produces one output. When the output is greater than `0.5`, the agent jumps; otherwise, it continues without jumping.

## Progressive Difficulty

The game difficulty increases as pipes are passed:

- Initial pipe speed: `3`
- Maximum pipe speed: `8`
- Pipe speed increases by `1` after every 10 pipes passed.
- The spacing between pipes decreases as the speed increases.

## AI Approaches

### NEAT Agent

The NEAT agent uses NeuroEvolution of Augmenting Topologies to evolve neural networks. The configuration described in the project report includes:

- Population size: `100`
- Number of inputs: `5`
- Number of outputs: `1`
- Activation function: `tanh`
- Weight mutation rate: `0.8`
- Connection-addition probability: `0.5`
- Node-addition probability: `0.2`
- Elitism: `2` individuals

The fitness function described in the report considers survival, alignment with the pipe gap, proximity to the ceiling or floor, and pipes passed.

### Heuristic Agent

The heuristic agent uses a manually defined rule based on the position of the bird and the centre of the next pipe gap. It does not learn through evolution.

## Reported Results

The project report records the following results:

| Metric | Reported result |
|---|---:|
| Heuristic agent average score | 54.7 pipes |
| Heuristic agent maximum score | 96 pipes |
| Heuristic agent minimum score | 30 pipes |
| NEAT agent maximum score | 135 pipes |
| NEAT agent best fitness | 4273.94 |

These values are the results documented in the project report.

## Technologies

- Python
- Pygame
- NEAT-Python
- Artificial neural networks
- Heuristic decision rules

## Project Context

**Course:** Artificial Intelligence  
**Institution:** ISMAT  
**Academic year:** 2025/2026


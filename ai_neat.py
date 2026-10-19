import pygame
import neat
import os
import sys
from flappy_bird import PIPE_GAP, Bird, Pipe, WIDTH, HEIGHT, FPS, PIPE_INTERVAL, WHITE, RED, BLUE, load_bird_frames

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - NEAT AI")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24, bold=True)

load_bird_frames()
generation = 0

# Histórico de gerações para o resumo final
historico = []


def eval_genomes(genomes, config):
    global generation
    generation += 1

    birds = []
    nets  = []
    ge    = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        birds.append(Bird())
        nets.append(net)
        ge.append(genome)

    pipes = [Pipe(WIDTH)]
    score = 0
    last_pipe_time = pygame.time.get_ticks()
    melhor_fitness_geracao = 0
    pipe_speed = 3

    while len(birds) > 0:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        now = pygame.time.get_ticks()
        # intervalo ajustado à velocidade atual
        intervalo_atual = max(1200, PIPE_INTERVAL - (pipe_speed - 3) * 200)

        if now - last_pipe_time > intervalo_atual:
            pipes.append(Pipe(WIDTH, pipe_speed))
            last_pipe_time = now

        for pipe in pipes:
            pipe.update()
        pipes = [p for p in pipes if not p.off_screen()]

        for i in range(len(birds) - 1, -1, -1):
            bird = birds[i]
            bird.update()

            ge[i].fitness += 0.1

           
            centro = HEIGHT / 2
            distancia_centro = abs(bird.y - centro) / HEIGHT
            ge[i].fitness -= distancia_centro * 0.3

            
            if bird.vel > 5:
                ge[i].fitness -= 0.2

            if pipes:
                next_pipe = None
                for p in pipes:
                    if p.x + p.width > bird.x:
                        next_pipe = p
                        break
                if next_pipe:
                    bird_cy = bird.y + bird.height / 2
                    in_gap = next_pipe.top_height < bird_cy < next_pipe.bottom_y
                    if in_gap:
                        ge[i].fitness += 0.4
                    else:
                        ge[i].fitness -= 0.3 

            inputs = bird.get_inputs(pipes)
            output = nets[i].activate(inputs)

            if output[0] > 0.5:
                bird.jump()

            bird_rect = bird.get_rect()
            dead = False
            for pipe in pipes:
                top, bottom = pipe.get_rects()
                if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
                    dead = True

            if bird.y > HEIGHT - 50 or bird.y < 0:
                dead = True

            if dead:
                # Atualiza melhor fitness da geração antes de remover
                if ge[i].fitness > melhor_fitness_geracao:
                    melhor_fitness_geracao = ge[i].fitness
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        for pipe in pipes:
            if not pipe.passed and len(birds) > 0 and pipe.x + pipe.width < birds[0].x:
                pipe.passed = True
                score += 1

                if score > 0 and score % 10 == 0:
                    pipe_speed = min(pipe_speed + 1, 15)  # limite máximo de 15
                    for p in pipes:
                        p.speed = pipe_speed  # atualiza canos já existentes

                for g in ge:
                    g.fitness += 10

        # Render
        screen.fill(BLUE)
        pygame.draw.rect(screen, (210, 180, 140), (0, HEIGHT - 40, WIDTH, 40))
        pygame.draw.rect(screen, (34, 139, 34), (0, HEIGHT - 45, WIDTH, 10))

        for pipe in pipes:
            pipe.draw(screen)
        for bird in birds:
            bird.draw(screen)

        screen.blit(font.render("Modo: NEAT",          True, WHITE), (10, 10))
        screen.blit(font.render(f"Geração: {generation}",        True, WHITE), (10, 40))
        screen.blit(font.render(f"Score: {score}",               True, WHITE), (10, 70))
        screen.blit(font.render(f"Velocidade: {pipe_speed}", True, WHITE), (10, 100))
        screen.blit(font.render(f"Pássaros vivos: {len(birds)}", True, WHITE), (10, 130))

        pygame.display.flip()

    # Calcular fitness de quem ainda estava vivo no fim
    for g in ge:
        if g.fitness > melhor_fitness_geracao:
            melhor_fitness_geracao = g.fitness

    fitness_todos = [g.fitness for g in ge] + []
    # Guardar dados desta geração no histórico
    historico.append({
        "geracao":        generation,
        "score":          score,
        "melhor_fitness": round(melhor_fitness_geracao, 2),
    })


def imprimir_resumo():
    separador = "═" * 52
    print(f"\n{separador}")
    print(f"  RESUMO DO TREINO — NEAT Flappy Bird")
    print(separador)
    print(f"  {'GER':>4}  {'SCORE':>6}  {'MELHOR FITNESS':>16}")
    print(f"  {'-'*4}  {'-'*6}  {'-'*16}")

    melhor_score_geral = 0
    melhor_geracao     = 1

    for h in historico:
        destaque = " ◄ melhor score" if h["score"] > melhor_score_geral else ""
        if h["score"] > melhor_score_geral:
            melhor_score_geral = h["score"]
            melhor_geracao     = h["geracao"]
        print(f"  {h['geracao']:>4}  {h['score']:>6}  {h['melhor_fitness']:>16}{destaque}")

    print(separador)
    print(f"  Total de gerações:  {len(historico)}")
    print(f"  Melhor score geral: {melhor_score_geral}  (geração {melhor_geracao})")
    print(f"{separador}\n")


def run_neat():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config_neat.txt")

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genomes, 50)

    # Imprimir resumo final
    imprimir_resumo()
    print(f"Melhor genoma:\n{winner}")


if __name__ == "__main__":
    run_neat()

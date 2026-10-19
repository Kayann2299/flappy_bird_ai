import pygame
import sys
import os
from flappy_bird import (
    Bird, Pipe, WIDTH, HEIGHT, FPS,
    PIPE_GAP, PIPE_INTERVAL, WHITE, BLUE, RED, GREEN,
    load_bird_frames
)


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird - Agente Heurístico")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24, bold=True)


load_bird_frames()


def decisao_heuristica(bird, pipes):
    """
    Comportamento 2: agente com regras definidas pelo programador.
    Salta se o pássaro estiver abaixo do centro da abertura do próximo cano.
    """
    next_pipe = None
    for p in pipes:
        if p.x + p.width > bird.x:
            next_pipe = p
            break

    if next_pipe is None:
        if bird.y > HEIGHT / 2:
            return True
        return False

    gap_center = next_pipe.top_height + (PIPE_GAP / 2)
    return bird.y > gap_center


def run_heuristico_headless():
    """
    Corre o agente heurístico sem janela gráfica.
    Retorna o score obtido.
    """
    bird = Bird()
    pipes = []
    score = 0
    pipe_speed = 3
    frame = 0

    while True:
        frame += 1

        # Gerar canos com base em frames em vez de milissegundos
        intervalo_frames = max(30, int((max(1200, PIPE_INTERVAL - (pipe_speed - 3) * 200)) / (1000 / FPS)))
        if frame % intervalo_frames == 0:
            pipes.append(Pipe(WIDTH, pipe_speed))

        for pipe in pipes:
            pipe.update()
        pipes = [p for p in pipes if not p.off_screen()]

        if decisao_heuristica(bird, pipes):
            bird.jump()

        bird.update()

        for pipe in pipes:
            if not pipe.passed and pipe.x + pipe.width < bird.x:
                pipe.passed = True
                score += 1
                if score > 0 and score % 10 == 0:
                    pipe_speed = min(pipe_speed + 1, 20)
                    for p in pipes:
                        p.speed = pipe_speed

        bird_rect = bird.get_rect()
        morreu = False
        for pipe in pipes:
            top, bottom = pipe.get_rects()
            if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
                morreu = True
                break
        if bird.y > HEIGHT - 50 or bird.y < 0:
            morreu = True

        if morreu:
            return score


def run_heuristico():
    bird = Bird()
    pipes = []
    score = 0
    last_pipe_time = pygame.time.get_ticks()
    pipe_speed = 3
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run_heuristico()
                    return

        now = pygame.time.get_ticks()
        intervalo_atual = max(1200, PIPE_INTERVAL - (pipe_speed - 3) * 200)
        if now - last_pipe_time > intervalo_atual:
            pipes.append(Pipe(WIDTH, pipe_speed))
            last_pipe_time = now

        for pipe in pipes:
            pipe.update()
        pipes = [p for p in pipes if not p.off_screen()]

        if decisao_heuristica(bird, pipes):
            bird.jump()

        bird.update()

        for pipe in pipes:
            if not pipe.passed and pipe.x + pipe.width < bird.x:
                pipe.passed = True
                score += 1
                if score > 0 and score % 10 == 0:
                    pipe_speed = min(pipe_speed + 1, 20)
                    for p in pipes:
                        p.speed = pipe_speed

        bird_rect = bird.get_rect()
        morreu = False
        for pipe in pipes:
            top, bottom = pipe.get_rects()
            if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
                morreu = True
        if bird.y > HEIGHT - 50 or bird.y < 0:
            morreu = True

        screen.fill(BLUE)
        pygame.draw.rect(screen, (210, 180, 140), (0, HEIGHT - 40, WIDTH, 40))
        pygame.draw.rect(screen, (34, 139, 34), (0, HEIGHT - 45, WIDTH, 10))

        for pipe in pipes:
            pipe.draw(screen)
        bird.draw(screen)

        screen.blit(font.render("Modo: Heurístico",          True, WHITE), (10, 10))
        screen.blit(font.render(f"Score: {score}",           True, WHITE), (10, 40))
        screen.blit(font.render(f"Velocidade: {pipe_speed}", True, WHITE), (10, 70))

        if morreu:
            msg  = font.render(f"Morreu! Score: {score}", True, RED)
            msg2 = font.render("R para reiniciar",        True, WHITE)
            screen.blit(msg,  (WIDTH // 2 - msg.get_width()  // 2, HEIGHT // 2 - 20))
            screen.blit(msg2, (WIDTH // 2 - msg2.get_width() // 2, HEIGHT // 2 + 20))
            pygame.display.flip()
            run_heuristico()
            return

        pygame.display.flip()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--tentativas", type=int, default=1,
                        help="Numero de tentativas headless (sem janela). Ex: python ai_heuristico_v2.py --tentativas 50")
    args = parser.parse_args()

    if args.tentativas > 1:
        print(f"A correr {args.tentativas} tentativas (modo headless)...")
        resultados = []
        for i in range(args.tentativas):
            score = run_heuristico_headless()
            resultados.append(score)
            print(f"  Tentativa {i+1:>2}: {score} canos")

        print()
        print("=" * 35)
        print(f"  Tentativas:   {len(resultados)}")
        print(f"  Melhor score: {max(resultados)}")
        print(f"  Pior score:   {min(resultados)}")
        print(f"  Media:        {sum(resultados)/len(resultados):.1f}")
        mediana = sorted(resultados)[len(resultados)//2]
        print(f"  Mediana:      {mediana}")
        print("=" * 35)
    else:
        run_heuristico()
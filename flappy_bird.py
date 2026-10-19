import pygame
import random
import sys
import os

BIRD_FRAMES = []

def load_bird_frames():
    global BIRD_FRAMES
    BIRD_FRAMES = []
    for i in range(1, 7):
        path = os.path.join(os.path.dirname(__file__), f"bird_{i}.png")
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            img = pygame.transform.scale(img, (80, 64))
            BIRD_FRAMES.append(img)
    print(f"Frames carregados: {len(BIRD_FRAMES)}")

# ── Configurações ──────────────────────────────────────────
WIDTH, HEIGHT = 400, 600
FPS = 60
GRAVITY = 0.3          # suave — cai mais devagar
JUMP_FORCE = -7        # salto controlado
PIPE_SPEED = 3         # canos mais lentos = mais tempo para reagir
PIPE_GAP = 150         # abertura generosa para aprender
PIPE_INTERVAL = 2500   # mais tempo entre canos

WHITE  = (255, 255, 255)
BLUE   = (50, 150, 235)
GREEN  = (34, 139, 34)
YELLOW = (255, 220, 0)
RED    = (220, 50, 50)
BLACK  = (0, 0, 0)

# ── Classe Pássaro ─────────────────────────────────────────
class Bird:
    def __init__(self, x=80, y=HEIGHT//2 - 30):
        self.x = x
        self.y = float(y)
        self.vel = 0.0
        self.width = 80
        self.height = 64
        self.alive = True
        self.score = 0
        self.fitness = 0
        self.frame_index = 0
        self.frame_timer = 0
        self.FRAME_SPEED = 8

    def jump(self):
        self.vel = JUMP_FORCE
        self.frame_index = 0
        self.frame_timer = 0

    def update(self):
        self.vel += GRAVITY
        self.vel = min(self.vel, 10)   # limita velocidade de queda máxima
        self.y += self.vel
        self.fitness += 1

    def get_rect(self):
        # hitbox menor que o sprite — mais justa
        return pygame.Rect(self.x + 16, self.y + 16, 48, 32)

    def draw(self, screen):
        if self.vel < 0:
            self.frame_timer += 1
            if BIRD_FRAMES and self.frame_timer >= self.FRAME_SPEED:
                self.frame_timer = 0
                if self.frame_index < len(BIRD_FRAMES) - 1:
                    self.frame_index += 1
        else:
            if BIRD_FRAMES:
                self.frame_index = len(BIRD_FRAMES) - 1

        if BIRD_FRAMES:
            screen.blit(BIRD_FRAMES[self.frame_index], (self.x, self.y))
        else:
            pygame.draw.ellipse(screen, YELLOW, (self.x, self.y, self.width, self.height))

    def get_inputs(self, pipes):
        """5 inputs para a rede neuronal"""
        next_pipe = None
        for p in pipes:
            if p.x + p.width > self.x:
                next_pipe = p
                break

        if next_pipe is None:
            return [0.0, 0.0, 1.0, self.vel / 10, self.y / HEIGHT]

        bird_cy = self.y + self.height / 2
        diff_top    = (bird_cy - next_pipe.top_height) / HEIGHT
        diff_bottom = (bird_cy - next_pipe.bottom_y) / HEIGHT
        dist_x      = (next_pipe.x - self.x) / WIDTH

        return [
            diff_top,           # distância ao topo do cano
            diff_bottom,        # distância ao fundo do cano
            dist_x,             # distância horizontal
            self.vel / 10,      # velocidade vertical
            self.y / HEIGHT     # altura absoluta
        ]

# ── Classe Cano ────────────────────────────────────────────
class Pipe:
    def __init__(self, x, speed=3):
        self.x = x
        self.width = 60
        self.speed = speed
        self.top_height = random.randint(120, HEIGHT - PIPE_GAP - 120)
        self.bottom_y = self.top_height + PIPE_GAP
        self.passed = False

    def update(self):
        self.x -= self.speed

    def get_rects(self):
        top    = pygame.Rect(self.x, 0, self.width, self.top_height)
        bottom = pygame.Rect(self.x, self.bottom_y, self.width, HEIGHT - self.bottom_y)
        return top, bottom

    def draw(self, screen):
        top, bottom = self.get_rects()
        pygame.draw.rect(screen, GREEN, top)
        pygame.draw.rect(screen, GREEN, bottom)
        pygame.draw.rect(screen, (0, 100, 0), (self.x - 5, self.top_height - 20, self.width + 10, 20))
        pygame.draw.rect(screen, (0, 100, 0), (self.x - 5, self.bottom_y, self.width + 10, 20))

    def off_screen(self):
        return self.x + self.width < 0

# ── Classe Jogo (modo humano) ──────────────────────────────
class FlappyBirdGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Flappy Bird - AI Project")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 28, bold=True)
        load_bird_frames()
        self.reset()

    def reset(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.last_pipe_time = pygame.time.get_ticks()

    def draw_background(self):
        self.screen.fill(BLUE)
        pygame.draw.rect(self.screen, (210, 180, 140), (0, HEIGHT - 40, WIDTH, 40))
        pygame.draw.rect(self.screen, (34, 139, 34), (0, HEIGHT - 45, WIDTH, 10))

    def run(self):
        while True:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.jump()
                    if event.key == pygame.K_r:
                        self.reset()
            self.update()
            self.render()

    def update(self):
        if not self.bird.alive:
            return
        self.bird.update()
        now = pygame.time.get_ticks()
        if now - self.last_pipe_time > PIPE_INTERVAL:
            self.pipes.append(Pipe(WIDTH))
            self.last_pipe_time = now
        for pipe in self.pipes:
            pipe.update()
            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.score += 1
        self.pipes = [p for p in self.pipes if not p.off_screen()]
        bird_rect = self.bird.get_rect()
        for pipe in self.pipes:
            top, bottom = pipe.get_rects()
            if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
                self.bird.alive = False
        if self.bird.y > HEIGHT - 50 or self.bird.y < 0:
            self.bird.alive = False

    def render(self):
        self.draw_background()
        for pipe in self.pipes:
            pipe.draw(self.screen)
        self.bird.draw(self.screen)
        self.screen.blit(self.font.render(f"Score: {self.score}", True, WHITE), (10, 10))
        if not self.bird.alive:
            msg = self.font.render("Morreu! R para reiniciar", True, RED)
            self.screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

if __name__ == "__main__":
    game = FlappyBirdGame()
    game.run()

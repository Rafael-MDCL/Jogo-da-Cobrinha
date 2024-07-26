import pygame
from pygame.locals import *
import random

# Define o tamanho da tela para o jogo e o tamanho do Pixel da cobrinha.
tamanho_janela = (600, 600)
tamanho_pixel = 10

# Função para criar colisão no corpo da cobrinha
def collision(pos1, pos2):
    return pos1 == pos2

# Função para limitar o movimento da cobrinha à tela do jogo
def off_limits(pos):
    return not (0 <= pos[0] < tamanho_janela[0] and 0 <= pos[1] < tamanho_janela[1])

# Função para posicionar a maçã de maneira aleatória, mas limitar ela pela tela do jogo
def random_on_grid():
    x = random.randint(0, (tamanho_janela[0] // tamanho_pixel) - 1) * tamanho_pixel
    y = random.randint(0, (tamanho_janela[1] // tamanho_pixel) - 1) * tamanho_pixel
    return x, y

# Inicializa o pygame e cria a tela do jogo
pygame.init()
screen = pygame.display.set_mode(tamanho_janela)
pygame.display.set_caption('Snake Game')

# Elementos do jogo
snake_pos = [(250, 50), (260, 50), (270, 50)]
snake_surface = pygame.Surface((tamanho_pixel, tamanho_pixel))
snake_surface.fill((255, 255, 255))
snake_direction = K_LEFT
next_direction = K_LEFT

# Elementos da maçã
apple_surface = pygame.Surface((tamanho_pixel, tamanho_pixel))
apple_surface.fill((255, 0, 0)) 
apple_pos = random_on_grid()

def restart_game():
    global snake_pos, apple_pos, snake_direction, next_direction
    snake_pos = [(250, 50), (260, 50), (270, 50)]
    snake_direction = K_LEFT
    next_direction = K_LEFT
    apple_pos = random_on_grid()

def is_opposite_direction(direction1, direction2):
    return (direction1 == K_UP and direction2 == K_DOWN) or \
           (direction1 == K_DOWN and direction2 == K_UP) or \
           (direction1 == K_LEFT and direction2 == K_RIGHT) or \
           (direction1 == K_RIGHT and direction2 == K_LEFT)

while True:
    pygame.time.Clock().tick(10)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()
        elif event.type == KEYDOWN:
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT]:
                if not is_opposite_direction(snake_direction, event.key):
                    next_direction = event.key
    
    # Atualiza a direção da cobrinha
    snake_direction = next_direction

    # Move a cobrinha
    head_x, head_y = snake_pos[0]
    if snake_direction == K_UP:
        new_head = (head_x, head_y - tamanho_pixel)
    elif snake_direction == K_DOWN:
        new_head = (head_x, head_y + tamanho_pixel)
    elif snake_direction == K_LEFT:
        new_head = (head_x - tamanho_pixel, head_y)
    elif snake_direction == K_RIGHT:
        new_head = (head_x + tamanho_pixel, head_y)

    # Checa se a cobrinha bateu nas bordas
    if off_limits(new_head):
        restart_game()

    # Checa se a cobrinha bateu no corpo
    if collision(new_head, snake_pos[0]) or new_head in snake_pos[1:]:
        restart_game()

    # Atualiza a posição da cobrinha
    snake_pos = [new_head] + snake_pos[:-1]

    # Checa se a cobrinha comeu a maçã
    if collision(new_head, apple_pos):
        snake_pos.append(snake_pos[-1])  # Adiciona um novo segmento à cobrinha
        apple_pos = random_on_grid()

    # Desenha a maçã e a cobrinha
    screen.blit(apple_surface, apple_pos)
    for pos in snake_pos:
        screen.blit(snake_surface, pos)

    pygame.display.update()

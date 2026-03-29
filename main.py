import random

import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

QUADRADO = 50
VELOCIDADE = 5

rodando = True

desired_direction = None
current_direction = None

matriz_posicao = []

historico = []


def init_game():
    global matriz_posicao, historico, current_direction, desired_direction

    matriz_posicao.clear()
    historico.clear()

    for i in range(3):
        matriz_posicao.append({'xy': [200, 100]})

    current_direction = None
    desired_direction = None


def pode_virar():
    head = matriz_posicao[0]['xy']
    return head[0] % QUADRADO == 0 and head[1] % QUADRADO == 0


def eventos():
    global rodando, desired_direction

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_h :
                print("cresceu")
                matriz_posicao.append({'xy': [200, 100]})
            if evento.key == pygame.K_k:
                print("gerou")
                gerar_frutas()
            if evento.key == pygame.K_UP and current_direction != 'down':
                desired_direction = 'up'
            if evento.key == pygame.K_DOWN and current_direction != 'up':
                desired_direction = 'down'
            if evento.key == pygame.K_LEFT and current_direction != 'right':
                desired_direction = 'left'
            if evento.key == pygame.K_RIGHT and current_direction != 'left':
                desired_direction = 'right'

fruta_gerada = False
fruta_position = [0,0]

def gerar_frutas():
    global matriz_posicao, historico, current_direction, desired_direction, fruta_gerada, fruta_position
    if not fruta_gerada:
        while True:
            h = random.randint(0, SCREEN_HEIGHT)
            y_final = h - h % QUADRADO
            w = random.randint(0, SCREEN_WIDTH)
            x_final = w - w % QUADRADO
            print(y_final)
            print(x_final)
            if not ([x_final, y_final] in matriz_posicao):
                break
        fruta_position = [x_final, y_final]
        fruta_gerada = True
    pygame.draw.rect(tela, "#00FF00", (fruta_position[0], fruta_position[1], QUADRADO, QUADRADO))




def andar_cobra():
    global current_direction, historico

    head = matriz_posicao[0]['xy']

    if pode_virar():
        current_direction = desired_direction

    if current_direction == 'up':
        head[1] -= VELOCIDADE
    elif current_direction == 'down':
        head[1] += VELOCIDADE
    elif current_direction == 'left':
        head[0] -= VELOCIDADE
    elif current_direction == 'right':
        head[0] += VELOCIDADE

    historico.insert(0, head.copy())

    for i in range(1, len(matriz_posicao)):
        atraso = i * (QUADRADO // VELOCIDADE)

        if atraso < len(historico):
            matriz_posicao[i]['xy'][0] = historico[atraso][0]
            matriz_posicao[i]['xy'][1] = historico[atraso][1]


def proc_colisoes():
    global fruta_gerada
    head = matriz_posicao[0]['xy']

    if (
        head[0] < 0 or
        head[0] + QUADRADO > SCREEN_WIDTH or
        head[1] < 0 or
        head[1] + QUADRADO > SCREEN_HEIGHT
    ):
        print("reset")
        init_game()

    for parte in matriz_posicao[1:]:
        if head == parte['xy'] and current_direction is not None:
            print("bateu no corpo")
            init_game()

    if head == fruta_position:
        fruta_gerada = False
        matriz_posicao.append({'xy': [-50, -50]})


def desenhar():


    for i, parte in enumerate(matriz_posicao):
        cor = "#000000" if i == 0 else "#F53737"
        pygame.draw.rect(tela, cor, (parte['xy'][0], parte['xy'][1], QUADRADO, QUADRADO))
    gerar_frutas()

if __name__ == '__main__':
    pygame.init()
    tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake")
    relogio = pygame.time.Clock()

    init_game()

    while rodando:
        tela.fill("#5050b9")
        eventos()
        andar_cobra()
        proc_colisoes()
        desenhar()
        # pygame.draw.rect(tela, '#00FF00', (0, 0, QUADRADO, QUADRADO))
        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()
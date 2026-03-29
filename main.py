import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

QUADRADO = 50
VELOCIDADE = 5

rodando = True

desired_direction = 'right'
current_direction = 'right'

matriz_posicao = []

historico = []


def init_game():
    global matriz_posicao, historico, current_direction, desired_direction

    matriz_posicao.clear()
    historico.clear()

    for i in range(3):
        matriz_posicao.append({'xy': [200 - i * QUADRADO, 100]})

    current_direction = 'right'
    desired_direction = 'right'


def pode_virar():
    head = matriz_posicao[0]['xy']
    return head[0] % QUADRADO == 0 and head[1] % QUADRADO == 0


def eventos():
    global rodando, desired_direction

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP and current_direction != 'down':
                desired_direction = 'up'
            if evento.key == pygame.K_DOWN and current_direction != 'up':
                desired_direction = 'down'
            if evento.key == pygame.K_LEFT and current_direction != 'right':
                desired_direction = 'left'
            if evento.key == pygame.K_RIGHT and current_direction != 'left':
                desired_direction = 'right'


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
        if head == parte['xy']:
            print("bateu no corpo")
            init_game()


def desenhar(tela):
    tela.fill("#5050b9")

    for i, parte in enumerate(matriz_posicao):
        cor = "#000000" if i == 0 else "#F53737"
        pygame.draw.rect(tela, cor, (parte['xy'][0], parte['xy'][1], QUADRADO, QUADRADO))


if __name__ == '__main__':
    pygame.init()
    tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake")
    relogio = pygame.time.Clock()

    init_game()

    while rodando:
        eventos()
        andar_cobra()
        proc_colisoes()
        desenhar(tela)

        pygame.display.flip()
        relogio.tick(FPS)

    pygame.quit()
import pygame
import random

# Inicializa la maquina de juego
pygame.init()

# El color del fondo
black = [ 0, 0, 0]
# El color de la estrella
white = [255,255,255]

# Creación de la ventana
Ancho, Alto = 860, 600
screen = pygame.display.set_mode((Ancho,Alto))

# Título e Icono
pygame.display.set_caption("Space Invaders")
icono = pygame.image.load('ufo.png')
pygame.display.set_icon(icono)

#Música
pygame.mixer.music.load("Blooming Villain.mp3")
pygame.mixer.music.play(-1)

# JUGADOR
player_img = pygame.image.load('Player.png')
posX, posY = Ancho/2.2, Alto - 80
cambio_X = 0
def player(x,y):
    screen.blit(player_img, (x, y))


# Enemigos
enemigolista = []
ene_X = []
ene_Y = []
eneX_cambio = []
eneY_cambio = []
numero_enemigos = 7

for i in range(numero_enemigos):
    enemigolista.append(pygame.image.load('Enemy.png'))
    ene_X.append(random.randint(0, 795))
    ene_Y.append(random.randint(0, 200))
    velocidad_horizontal = 1.61
    velocidad_vertical = 30
    eneX_cambio.append(velocidad_horizontal)
    eneY_cambio.append(velocidad_vertical)

def enemigo(x, y, i):
    screen.blit(enemigolista[i], (x, y))


# Laser
laser_img = pygame.image.load('bullet.png')
laser_X, laser_Y = 0, Alto - 80
laserX_cambio = 0
laserY_cambio = 5
laser_state = 0 #estado no visible

def disparo(x, y):
  global laser_state
  laser_state = 1 # estado movible
  screen.blit(laser_img, (x+16,y+10)) #dibuja la bala  se agrega valores a la coordenada para que el laser salga del meido de la nave


'''Colision: Para armar la colision entre el laser y el enemigo, aplicaremos
la formula de distancia entre ellos y así ver si es lo suficientemente pequeño
para que desaparezca.'''
def colision(a, b, c, d):
    distancia = (((a - c)**2)+((b - d)**2))**(1/2)
    if distancia < 27:
        return True
    else:
        return False


# Mostrar los puntos obtenidos en pantalla
puntaje = 0
texto = pygame.font.SysFont("comicsans", 30)
texto_X = 20
texto_Y = 20
def mostrar_puntaje(x, y):
    puntos = texto.render("Puntos: " + str(puntaje), True, (255, 255, 255))
    screen.blit(puntos, (x, y))


# vidas
vida = 5
v_texto = pygame.font.SysFont("comicsans", 30)
vidas_X = 20
vidas_Y = 40
def mostrar_vidas(x, y):
    vidas = v_texto.render("Vidas: " + str(vida), True, (255, 255, 255))
    screen.blit(vidas, (x, y))


fin = pygame.font.SysFont("comicsans", 50 )
def fin_juego():
    mensaje = fin.render("GAME OVER", True, (255, 255, 255))
    screen.blit(mensaje, (Ancho//2 - 170, Alto//2 - 60))
    quit()


# Crea un arreglo vacío para las estrellas
list_estrella = []
# Repite 100 veces adicionando una estrella de nieve en una posición aleatoria x,y
for i in range(100):
    x=random.randrange(0, Ancho)
    y=random.randrange(0, Alto)
    list_estrella.append([x, y])


clock = pygame.time.Clock()
# Loop
juego = True
while juego:
    # Color de la ventana
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            juego = False

        if event.type == pygame.KEYDOWN:    # Al presionar la tecla
            if event.key == pygame.K_RIGHT:  # Mover a la derecha en el plano
                 cambio_X = 3
            if event.key == pygame.K_LEFT:  # Mover a la izquierda en el plano
                cambio_X = -3
            if event.key == pygame.K_SPACE or event.key == pygame.K_x:  # Al presionar la barra o "x" se ejecuta la función
                if laser_state == 0:    # Para que al mover la nave y presionar varias veces el disparo no se regenera antesde su limite
                    laser_X = posX
                    disparo(laser_X, laser_Y)    # posicion de la nave actual en x, posicion y de la nave

                #al ejecutarse esto, cambia el estado del laser 0 a 1
                #surgen dos problemas: 1. solos se dispara una vez
        if event.type == pygame.KEYUP: #Al de jar de presionarlo
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                cambio_X = 0


    # Estrella
    for i in range(len(list_estrella)):
        # Dibujamos la estrella
        pygame.draw.circle(screen, white, list_estrella[i], 2)

        # Movimiento de la estrella: un pixel hacia abajo
        list_estrella[i][1] += 1

        # Si la estrella se mueve más allá del limite inferior de la
        # ventana
        if list_estrella[i][1] > Alto:
            # La mueve de nuevo a la parte superior de la ventana
            y=random.randrange(-50, -10)
            list_estrella[i][1] = y
            # Da a esta una nueva posición x
            x=random.randrange(0, Ancho)
            list_estrella[i][1] = x

    # Movimiento horizonal de la nave
    posX += cambio_X

    #Condición para que la nave no pase la pantalla
    if posX < 0:
        posX = 0
    elif posX >= 795:
        posX = 795

    # Movimiento del enemigo
    for i in range(numero_enemigos):
        ene_X[i] += eneX_cambio[i]
        # ene_Y[i] += eneY_cambio[i]
        # Condición para que el enemigo no salga de la pantalla
        if ene_X[i] <= 0:
            eneX_cambio[i] = velocidad_horizontal
            ene_Y[i] += velocidad_vertical
        elif ene_X[i] >= 795:
            eneX_cambio[i] = -velocidad_horizontal
            ene_Y[i] += velocidad_vertical

    for i in range(numero_enemigos):
        if ene_Y[i] >= 550 and vida > 0:
            vida -= 1
        elif ene_Y[i] >= 550 and vida == 0:
            for vm in range(numero_enemigos):
                ene_Y[vm] = 4000
            posY = 4000
            fin_juego()


        # colision
        choque = colision(ene_X[i], ene_Y[i], laser_X, laser_Y)
        if choque:
            laser_Y = Alto - 80
            laser_state = 0
            puntaje += 1
            ene_X[i], ene_Y[i] = random.randint(0, 795), random.randint(0, 200)
        enemigo(ene_X[i], ene_Y[i], i)

    #Movimiento del laser
    #solucion 1:
    if laser_Y <= 0:
        laser_Y = 480
        laser_state = 0
    #solución 1
    if laser_state == 1:
        disparo(laser_X, laser_Y)
        laser_Y -= laserY_cambio

    player(posX, posY)
    mostrar_vidas(vidas_X, vidas_Y)
    mostrar_puntaje(texto_X, texto_Y)

    # Actualiza la ventana con lo que se ha dibujado.
    pygame.display.update()
    clock.tick(200)


pygame.quit ()

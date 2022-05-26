import pygame
from pygame.locals import *
import random

pygame.init()

# Simbolo PyGame
programIcon = pygame.image.load('flappy-dunk.png')
pygame.display.set_icon(programIcon)

#Gera tela principal
WIDTH = 1024
HEIGHT = 768
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Dunk')

#fonte do texto
fonte = pygame.font.SysFont("Bauhaus 93", 60)

#cores
branco = (255,255,255)

#Variáveis
bg_movimento = 0
movimento_velocidade = -4
voar = False
game_over = False
movimento_tela = False
continuar = True
anel_frequencia = 3500
ultimo_anel = pygame.time.get_ticks() - anel_frequencia
placar = 0
passar_anel = False
asa_frequencia = 30

clock = pygame.time.Clock()
fps = 60


bg = pygame.image.load('background.jpg').convert()
bg = pygame.transform.scale(bg,(WIDTH,HEIGHT))
bg_rect = bg.get_rect()
bg_rect2 = bg_rect.copy()

botao_img = pygame.image.load('bola.png')


def texto (text, fonte, text_col, x, y):
    img = fonte.render(text, True, text_col)
    window.blit(img,  (x,y))

def reseta_jogo():
    anel_grupo.empty
    anel_grupo1.empty
    anel_em_cima.kill()
    anel_embaixo.kill()
    ball.rect.x = 120
    ball.rect.y = int(HEIGHT/2) + 8
    asa_direita.rect.x = 183
    asa_direita.rect.y = int(HEIGHT/2)-20
    asa_esquerda.rect.x = 145
    asa_esquerda.rect.y = int(HEIGHT/2)-15
    placar = 0
    return placar

class Bola(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bola.png')
        self.image = pygame.transform.scale(self.image,(60,60))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.speedy = 0
    
    def update(self):

        #gravidade
        if voar == True:
            self.speedy += 0.5
            if self.speedy > 10:
                self.speedy = 10
            if self.rect.bottom < 781:
                self.rect.y += int(self.speedy)

       
class Asa(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.image = pygame.image.load('Asa virada.png')
        self.images.append(self.image)
        self.image = pygame.image.load('Asa.png')
        self.images.append(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.speedy = 0
    
    def update(self): 
        #gravidade
        if voar == True:
            self.speedy += 0.5
            if self.speedy > 10:
                self.speedy = 10
            if self.rect.bottom < 781:
                self.rect.y += int(self.speedy)
    def abaixado(self,x):
        self.image = self.images[0]
        self.rect.center = [x,self.rect.centery-15]

    def levantado(self,x):
        self.image = self.images[1]
        self.rect.center = [x,self.rect.centery+15]


class Anel(pygame.sprite.Sprite):
    def __init__(self,x,y,posicao):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Anel em cima.png')
        self.rect = self.image.get_rect()
        if posicao == 1:
            self.image = pygame.image.load('Anel Embaixo.png')
            self.rect.bottomleft = [x,y]
        if posicao == -1:
            self.rect.topleft = [x,y]

    def update(self):
        #velocidade
        if voar == True:
            self.rect.x += movimento_velocidade
        if self.rect.right < 0:
            self.kill()

class Botao():
    def __init__(self,x,y,image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    
    def draw(self):

        acao = False

        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                acao = True

        window.blit(self.image,(self.rect.x, self.rect.y))
            
        return acao

#grupos
anel_grupo = pygame.sprite.Group()
anel_grupo1 = pygame.sprite.Group()
asa_grupo = pygame.sprite.Group()
bola_grupo = pygame.sprite.Group()
asa_grupo_atras = pygame.sprite.GroupSingle()

#posição dos sprites
asa_direita = Asa(183, int(HEIGHT/2)-20)
asa_esquerda = Asa(145, int(HEIGHT/2)-15)
ball = Bola(150, int(HEIGHT/2))

#adicionando os sprites aos grupos
asa_grupo_atras.add(asa_direita)
asa_grupo.add(asa_esquerda)
bola_grupo.add(ball)

botao_reiniciar = Botao(WIDTH // 2 - 50, HEIGHT // 2 - 100, botao_img)

#Loop principal
game = True
while game:

    clock.tick(60)

    window.blit(bg,bg_rect)
    window.blit(bg, bg_rect2)

    anel_grupo.draw(window)
    asa_grupo_atras.draw(window)
    bola_grupo.draw(window)
    asa_grupo.draw(window)
    anel_grupo1.draw(window)

    asa_grupo_atras.update()
    bola_grupo.update()
    asa_grupo.update()
    anel_grupo.update()
    anel_grupo1.update()

    #if pygame.sprite.collide_rect(ball.rect.right, anel.rect.left):
            #game_over = True

    #Checa se a bola tocou o chão ou o teto
    if ball.rect.bottom > 710:
        game_over = True
        voar = False
        movimento_tela = False

    if ball.rect.top < 61:
        game_over = True
        movimento_tela = False  
        voar = False
        continuar = False

    #checar o placar
    if len(anel_grupo) > 0:
        if bola_grupo.sprites()[0].rect.center == anel_grupo.sprites()[0].rect.center:
            placar+=1
    
    texto(str(placar), fonte, branco, 512, 20)

    pygame.display.flip()
    if voar == True:
        time_now = pygame.time.get_ticks()
        if time_now - ultimo_anel > anel_frequencia:
            anel_height = random.randint(384,810)
            anel_em_cima = Anel(1000, anel_height - 426,-1)
            anel_embaixo = Anel(1000, anel_height, 1)
            anel_grupo.add(anel_em_cima)
            anel_grupo1.add(anel_embaixo)
            ultimo_anel = time_now 
    
            #if pygame.sprite.groupcollide(bola_grupo,anel_grupo1,False, False):
                #movimento_velocidade = 4
                #tempo = pygame.time.set_timer(event, millis=10)
                #if tempo == 10:
                    #movimento_velocidade = -4
                    #pygame.time.set_timer(event,millis = 0)


    if movimento_tela == True:
        bg_rect.x += movimento_velocidade
        if bg_rect.right < 0:
            bg_rect.x += bg_rect.width
        bg_rect2.x = bg_rect.x + bg_rect2.width
    
    if game_over == True:
        if botao_reiniciar.draw() == True:
            game_over = False
            continuar = True
            placar = reseta_jogo()
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if continuar == True:
                if event.key == pygame.K_SPACE and game_over == False:
                    voar = True
                    movimento_tela = True
                    ball.speedy = -10
                    asa_esquerda.speedy = -10
                    asa_direita.speedy = -10
                    asa_esquerda.abaixado(140)
                    asa_direita.abaixado(165)
        if event.type == pygame.KEYUP:
            if continuar == True:
                if event.key == pygame.K_SPACE and game_over == False:
                    asa_esquerda.levantado(145)
                    asa_direita.levantado(180)

        if event.type == pygame.QUIT:
            game = False

    

    pygame.display.update()


pygame.quit()
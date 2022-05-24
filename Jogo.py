import pygame
from pygame.locals import *
import random

pygame.init()


#Gera tela principal
WIDTH = 1024
HEIGHT = 768
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Dunk')

#Variáveis
bg_movimento = 0
movimento_velocidade = -4
voar = False
game_over = False
movimento_tela = False
continuar = True
anel_frequencia = 3500
ultimo_anel = pygame.time.get_ticks() - anel_frequencia

clock = pygame.time.Clock()
fps = 60


bg = pygame.image.load('background.jpg').convert()
bg = pygame.transform.scale(bg,(WIDTH,HEIGHT))
bg_rect = bg.get_rect()
bg_rect2 = bg_rect.copy()

class Bola(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('bola.png')
        self.image = pygame.transform.scale(self.image,(70,70))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.speedy = 0
    
    def update(self):

        #gravidade
        if voar == True:
            self.speedy += 0.5
            if self.speedy > 10:
                self.speedy = 10
            if self.rect.bottom < 708:
                self.rect.y += int(self.speedy)

       
class Assa_esquerda(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Asa esquerda.png')
        self.image = pygame.transform.scale(self.image,(90,90))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.speedy = 0
    
    def update(self):
        #gravidade
        if voar == True:
            self.speedy += 0.5
            if self.speedy > 10:
                self.speedy = 10
            if self.rect.bottom < 708:
                self.rect.y += int(self.speedy)

class Anel(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('anel.png')
        self.image = pygame.transform.scale(self.image,(1500,900))
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    def update(self):
        #velocidade
        if voar == True:
            self.rect.x += movimento_velocidade
        if self.rect.right < 0:
            self.kill()
            
            

#grupos
anel_grupo = pygame.sprite.Group()
assa_grupo = pygame.sprite.Group()
bola_grupo = pygame.sprite.Group()
assa_grupo_atras = pygame.sprite.GroupSingle()

#posição dos sprites
assa_direita = Assa_esquerda(183, int(HEIGHT/2)-20)
assa_esquerda = Assa_esquerda(145, int(HEIGHT/2)-15)
ball = Bola(150, int(HEIGHT/2))

#adicionando os sprites aos grupos
assa_grupo_atras.add(assa_direita)
assa_grupo.add(assa_esquerda)
bola_grupo.add(ball)

        

#Loop principal
game = True
while game:

    clock.tick(60)

    window.blit(bg,bg_rect)
    window.blit(bg, bg_rect2)

    anel_grupo.draw(window)
    assa_grupo_atras.draw(window)
    bola_grupo.draw(window)
    assa_grupo.draw(window)

    assa_grupo_atras.update()
    bola_grupo.update()
    assa_grupo.update()
    anel_grupo.update()

    #Checa se a bola tocou o chão ou o teto
    if ball.rect.bottom > 708:
        game_over = True
        voar = False
        movimento_tela = False
    if ball.rect.top < 60:
        game_over = False
        movimento_tela = False
        voar = False
        continuar = False

    pygame.display.flip()
    if voar == True:
        time_now = pygame.time.get_ticks()
        if time_now - ultimo_anel > anel_frequencia:
            anel_height = random.randint(-100,100)
            anel = Anel(WIDTH, int(HEIGHT/2)+anel_height)
            anel_grupo.add(anel)
            ultimo_anel = time_now 

    if movimento_tela == True:
        bg_rect.x += movimento_velocidade
        if bg_rect.right < 0:
            bg_rect.x += bg_rect.width
        bg_rect2.x = bg_rect.x + bg_rect2.width
    
    
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if continuar == True:
                if event.key == pygame.K_SPACE and game_over == False:
                    voar = True
                    movimento_tela = True
                    ball.speedy = -10
                    assa_esquerda.speedy = -10
                    assa_direita.speedy = -10

        if event.type == pygame.QUIT:
            game = False

    

    pygame.display.update()


pygame.quit()
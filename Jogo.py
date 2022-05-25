from turtle import width
import pygame
from pygame.locals import *
import random

pygame.init()


#Gera tela principal
WIDTH = 1024
HEIGHT = 850
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

clock = pygame.time.Clock()
fps = 60


bg = pygame.image.load('background.jpg').convert()
bg = pygame.transform.scale(bg,(WIDTH,HEIGHT))
bg_rect = bg.get_rect()
bg_rect2 = bg_rect.copy()

def texto (text, fonte, text_col, x, y):
    img = fonte.render(text, True, text_col)
    window.blit(img,  (x,y))

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
            if self.rect.bottom < 781:
                self.rect.y += int(self.speedy)

       
class Asa_esquerda(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        self.image = pygame.image.load('Asa esquerda.png')
        self.images.append(self.image)
        self.image = pygame.image.load('Asa esquerda virada.png')
        self.images.append(self.image)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.speedy = 0
    
    def update(self):
        #animação
        self.counter += 1
        asa_cooldown = 15

        if self.counter > asa_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]
        
        #gravidade
        if voar == True:
            self.speedy += 0.5
            if self.speedy > 10:
                self.speedy = 10
            if self.rect.bottom < 781:
                self.rect.y += int(self.speedy)

class Anel(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('anel.png')
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
asa_grupo = pygame.sprite.Group()
bola_grupo = pygame.sprite.Group()
asa_grupo_atras = pygame.sprite.GroupSingle()

#posição dos sprites
asa_direita = Asa_esquerda(183, int(HEIGHT/2)-20)
asa_esquerda = Asa_esquerda(145, int(HEIGHT/2)-15)
ball = Bola(150, int(HEIGHT/2))

#adicionando os sprites aos grupos
asa_grupo_atras.add(asa_direita)
asa_grupo.add(asa_esquerda)
bola_grupo.add(ball)


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

    asa_grupo_atras.update()
    bola_grupo.update()
    asa_grupo.update()
    anel_grupo.update()

    #if pygame.sprite.collide_rect(ball.rect.right, anel.rect.left):
            #game_over = True

    #Checa se a bola tocou o chão ou o teto
    if ball.rect.bottom > 781:
        game_over = True
        voar = False
        movimento_tela = False
    if ball.rect.top < 72:
        game_over = False
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
            anel_height = random.randint(0,350)
            anel = Anel(2000, int(HEIGHT/2)+anel_height)
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
                    asa_esquerda.speedy = -10
                    asa_direita.speedy = -10

        if event.type == pygame.QUIT:
            game = False

    

    pygame.display.update()


pygame.quit()
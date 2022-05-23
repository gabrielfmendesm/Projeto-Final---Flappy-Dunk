import pygame
from pygame.locals import *

pygame.init()


#Gera tela principal
WIDTH = 1024
HEIGHT = 768
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Dunk')

bg_movimento = 0
movimento_velocidade = -4

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


bola_grupo = pygame.sprite.Group()

ball = Bola(150, int(HEIGHT/2))
bola_grupo.add(ball)
        

#Loop principal
game = True
while game:

    clock.tick(60)
    
    bg_rect.x += movimento_velocidade
    if bg_rect.right < 0:
        bg_rect.x += bg_rect.width
    bg_rect2.x = bg_rect.x + bg_rect2.width

    window.blit(bg,bg_rect)
    window.blit(bg, bg_rect2)

    bola_grupo.draw(window)


    pygame.display.flip()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    

    pygame.display.update()


pygame.quit()
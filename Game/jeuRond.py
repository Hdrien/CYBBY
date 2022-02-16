import pygame
from pygame.locals import *

i = 512
j = 384
pos = (i, j)
red = (255, 0, 0)
similired = (200, 50, 50)
similiwhite = (150, 150, 150)
white = (255, 255, 255)
black = (0, 0, 0)
radius_min = 100
radius_max = 350
speed = 60
thick = 30
thin = 10

score = 0
scoreHelper = 20


class circle:
    def __init__(self, x, y, color, radius, thickness):
        self.pos = (x, y)
        self.color = color
        self.radius = radius
        self.thickness = thickness


# the 2 circles initiation
rondFixe = circle(i, j, red, radius_max, thick)
rond = circle(i, j, white, radius_min, thin)

# Background
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (1024, 7268))
fenetre = pygame.display.set_mode((1024, 768))

fenetre.blit(background, (0, 0))

# text (for score display)
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
scoreText = str(score // 20)
textsurface = myfont.render(scoreText, False, (0, 0, 0))
fenetre.blit(textsurface, (0, 0))

# drawing
rondDessin = pygame.draw.circle(fenetre, rond.color, rond.pos, rond.radius, rond.thickness)
rondFixeDessin = pygame.draw.circle(fenetre, rondFixe.color, rondFixe.pos, rondFixe.radius, rondFixe.thickness)
pygame.display.update()

continuer = 1

# clock
clock = pygame.time.Clock()

while continuer:

    clock.tick(speed)
    scoreText = str(score // 20)

    if ((rond.radius - rond.thickness) >= (rondFixe.radius - rondFixe.thickness)) and (
            (rond.radius + rond.thickness) <= (rondFixe.radius + rondFixe.thickness / 2)):

        rondFixe.color = similired
        rond.color = similiwhite

        fenetre.blit(background, (0, 0))
        textsurface = myfont.render(scoreText, False, (0, 0, 0))
        fenetre.blit(textsurface, (0, 0))
        rondFixeDessin = pygame.draw.circle(fenetre, rondFixe.color, rondFixe.pos, rondFixe.radius,
                                            rondFixe.thickness)
        rondDessin = pygame.draw.circle(fenetre, rond.color, rond.pos, rond.radius, rond.thickness)
        pygame.display.update()

        score += 1
        if score == scoreHelper:
            scoreHelper += 20

    else:
        rondFixe.color = red
        rond.color = white

        fenetre.blit(background, (0, 0))
        textsurface = myfont.render(scoreText, False, (0, 0, 0))
        fenetre.blit(textsurface, (0, 0))
        rondFixeDessin = pygame.draw.circle(fenetre, rondFixe.color, rondFixe.pos, rondFixe.radius,
                                            rondFixe.thickness)
        rondDessin = pygame.draw.circle(fenetre, rond.color, rond.pos, rond.radius, rond.thickness)
        pygame.display.update()

    for event in pygame.event.get():

        if event.type == KEYDOWN and event.key == K_SPACE:
            continuer = 0

        if event.type == KEYDOWN and event.key == K_UP:
            rond.radius += 10
            fenetre.blit(background, (0, 0))
            rondFixeDessin = pygame.draw.circle(fenetre, rondFixe.color, rondFixe.pos, rondFixe.radius,
                                                rondFixe.thickness)
            rondDessin = pygame.draw.circle(fenetre, rond.color, rond.pos, rond.radius, rond.thickness)
            pygame.display.update()

        if event.type == KEYDOWN and event.key == K_DOWN:
            rond.radius -= 10
            fenetre.blit(background, (0, 0))
            rondFixeDessin = pygame.draw.circle(fenetre, rondFixe.color, rondFixe.pos, rondFixe.radius,
                                                rondFixe.thickness)
            rondDessin = pygame.draw.circle(fenetre, rond.color, rond.pos, rond.radius, rond.thickness)
            pygame.display.update()

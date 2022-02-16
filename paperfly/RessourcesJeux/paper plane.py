import  pygame
import time
from random import*


blue = (113,177,227) #valeur max =255.
white = (255,255,255)

pygame.init()

surfaceW = 1000
surfaceH = 500
ballonW = 150
ballonH = 150
nuageW = 74
nuageH = 170


surface = pygame.display.set_mode((surfaceW,surfaceH))
pygame.display.set_caption("Ballon Volant")
clock = pygame.time.Clock()

img_nuage01 = pygame.image.load('ring56.png')
img = pygame.image.load('plane45.png')
img_nuage02 = pygame.image.load('ring12.png')

def score(compte) :
    police = pygame.font.Font('BradBunR.ttf', 16)
    texte = police.render("score : " + str(compte), True, white)
    surface.blit(texte, [10,0])

def nuages1(x_nuage, y_nuage):
    surface.blit(img_nuage01, (x_nuage, y_nuage))


def nuages2(x_nuage, y_nuage):

    surface.blit(img_nuage02,(x_nuage+38,y_nuage))

def rejoueOuQuitte():
    for event in pygame.event.get([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT]):
        if event.type == pygame.QUIT :
            pygame.quit()
            quit()
        elif event.type ==pygame.KEYUP:
            continue
        return event.key

    return  None

def creaTexteObjs (texte, font):
    texteSurface = font.render(texte,True,white)
    return texteSurface, texteSurface.get_rect()


def msgSurface (texte):
    GOTexte = pygame.font.Font('BradBunR.ttf', 150)
    petitTexte = pygame.font.Font('BradBunR.ttf',20)

    titreTexteSurf, titreTexteRect = creaTexteObjs(texte, GOTexte)
    titreTexteRect.center = surfaceW/2,((surfaceH/2)-50)
    surface.blit(titreTexteSurf, titreTexteRect)

    petitTexteSurf, petitTexteRect = creaTexteObjs\
        ("appuyer sur une touche pour continuer", petitTexte )
    petitTexteRect.center = surfaceW/2, ((surfaceH/2) +50)
    surface.blit(petitTexteSurf, petitTexteRect)

    pygame.display.update()
    time.sleep(2)

    while rejoueOuQuitte() == None :
        clock.tick()

    main()

def gameOver():
    msgSurface("Oups!")

def ballon(x,y, image):
    surface.blit(image, (x,y))



def main():
    x=150
    y=200
    y_move=0

    x_nuage = surfaceW
    y_nuage = randint(10,25)
    #espace = ballonH*3
    nuage_vitesse = 6

    score_actuel = 0

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over= True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_move = -15
                    y += y_move

            if event.type ==pygame.KEYUP :
                if event.key == pygame.K_DOWN:
                    y_move = 15
                    y += y_move


        surface.fill(blue)
        nuages1(x_nuage, y_nuage)
        ballon(x,y,img)
        nuages2(x_nuage, y_nuage)


        score(score_actuel)

        x_nuage -=nuage_vitesse

        if y < -40:
            y= -40
        if y>surfaceH -115:
            y= surfaceH-115


        if x_nuage < (-1*nuageW):
            x_nuage = surfaceW
            y_nuage = randint(0,330)


        if x +ballonW > x_nuage :
            if y >= y_nuage and y+ballonH <= y_nuage+nuageH+100:
                if x + ballonW > x_nuage and x +ballonH < x_nuage + nuageW:
                    print("un anneau a ete ramasser")

                    score_actuel +=1
                    #gameOver()





        pygame.display.update()
        clock.tick(40)


main()
pygame.quit()
quit()
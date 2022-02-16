import  pygame
import time
from random import*

#initialisation de la partie
blue = (113,177,227) #valeur max =255.
white = (255,255,255)

pygame.init()

#initialisation des elements de la partie, taille de l'ecran, bouteille, verres
surfaceW = 1000
surfaceH = 500
bouteilleW = 200
bouteilleH = 200
verreW = 74
verreH = 170
check = True



surface = pygame.display.set_mode((surfaceW,surfaceH))
pygame.display.set_caption("BouteilleVolant")
clock = pygame.time.Clock()

img_verre01 = pygame.image.load('glass.png')
img = pygame.image.load('bouteille.png')


def score(compte) :
    police = pygame.font.Font('BradBunR.ttf', 16)
    texte = police.render("score : " + str(compte), True, white)
    surface.blit(texte, [10,0])

def timer(compte) :
    police = pygame.font.Font('BradBunR.ttf', 16)
    texte = police.render('temps:' + str(compte), True, white)
    surface.blit(texte, [100,0])

def verres1(x_verre, y_verre):
    surface.blit(img_verre01, (x_verre, y_verre))



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
    GOTexte = pygame.font.Font('BradBunR.ttf', 75)
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

    #main()

def gameOver():
    msgSurface("Temps ecoule!")

def bouteille(x,y, image):
    surface.blit(image, (x,y))



def main():
    game_over = False
    while not game_over:


        i = 1
        j = 1
        nbre_equipe = 2
        nbre_joueur = 3
        x=350
        y=50
        y_move=0


        x_verre = randint(10,300)
        y_verre =250
        #espace = bouteilleH*3
        score_actuel = 0


        start_ticks=pygame.time.get_ticks()

        while j <= nbre_equipe:
            surface.fill(blue)
            if j == 1:
                msgSurface("Premier joueur de l'equipe 1")

            if j == 2:
                i =0
                msgSurface("Premier joueur de l'equipe 2")


            while i < nbre_joueur:

                seconds = 60-(pygame.time.get_ticks() - start_ticks) / 1000
                if seconds ==0:
                    gameOver()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_over= True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            x_move = -15
                            x += x_move

                    if event.type ==pygame.KEYUP :
                        if event.key == pygame.K_RIGHT:
                            x_move = 15
                            x += x_move


                surface.fill(blue)
                verres1(x_verre, y_verre)
                bouteille(x,y,img)



                score(score_actuel)
                timer(seconds)



                if y < -40:
                    y= -40
                if y>surfaceH -115:
                    y= surfaceH-115




                if y +bouteilleH <=y_verre :
                    if x >= x_verre-25 and x+bouteilleW <= x_verre+325:
                        print(score_actuel)
                        score_actuel +=1
                            #gameOver()





                pygame.display.update()
                clock.tick(40)

                #print(seconds)
                if score_actuel == 50:
                    i = i + 1
                    if i == 2:
                        msgSurface("Joueur 2 c'est a vous")

                    if i == 3:
                        msgSurface("Joueur 3 c'est a vous")

                    if i == 4:
                        msgSurface("Joueur 4 c'est a vous")

                    if i == 5:
                        msgSurface("Joueur 5 c'est a vous")

                    if i == 6:
                        msgSurface("Joueur 6 c'est a vous")

                    if i == 7:
                        msgSurface("Joueur 7 c'est a vous")

                    if i == 8:
                        msgSurface("Joueur 8 c'est a vous")

                    score_actuel =0
                    surface.fill(blue)

            j=j+1
        gameOver()

main()
pygame.quit()
quit()

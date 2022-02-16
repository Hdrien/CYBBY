# coding=utf-8
from Tkinter import *  # Bibliotheque de jeu
import random
import os
import time
import sys
import serial  # communication arduino
import RPi.GPIO as GPIO  # Boutons sur GPIO

# ======================================================================
#                               HOW TO
# ======================================================================

# Les valeurs MAX du theremine sont calculées dans ready1 et ready2
# La frequence est lu en continue de l'arduino par read() (toutes les 10ms car l'arduino ne calcule qu'une nouvelle fréquence toute les 10ms)

# Tu peux faire CTRL+! et CTRL+MAJ+! pour t'y retrouver et naviguer plus rapidement dans le code, essaye tu verra
# S'il te fait une erreur du style "expected an indented block" tu va dans la barre des menus "Document>replace Tabs By Spaces" et ca marchera après

affichageFreqence = False  # Mets ça a True si tu veux voir les frequences s'afficher
debug = False  # Pour afficher plus d'informations en console

# ======================================================================
#                               ARDUINO
# ======================================================================
# Initialisation des variables de communication
usb_port = serial.Serial('/dev/ttyAMA0', 57600, timeout=1)
usb_port.open()

freq = -1


# Lecture en continue depuis l'arduino dans la variable globale freq
def read():
    global freq
    usb = usb_port.readline()
    if (usb != '' and usb != '\n' and usb != '\c' and usb != '\r' and usb != '\cr' and usb != '\lf'):
        try:
            # Tentative de bornage des mesure pour éviter les écarts trop grands des instabilités
            # ~ if int(usb)<4000 and -100<int(usb)-freq<100:
            # ~ freq = int(usb)
            # ~ if int(usb)<40:
            freq = int(usb)
        except ValueError:
            print "error read"
    if (affichageFreqence): print freq

    # Cette fonction se répete toute les 10ms (car l'arduino envoie des données toutes les 10ms)
    root.after(10, read)


# ======================================================================
#                               BOUTONS
# ======================================================================
GPIO.setmode(GPIO.BCM)
EnterPin = 18  # 18 BCM ; 12 board     Orange
ChoicePin = 24  # 24 BCM ; 18 board     Jaune
GPIO.setup(EnterPin, GPIO.IN)  # Orange : ENTER
GPIO.setup(ChoicePin, GPIO.IN)  # Jaune : CHOIX

BtnChoix = False
BtnEnter = False
channel = 0
call = False


# ----------------------------------------------------------------------
# Fonction qui gère tous les boutons------------------------------------
# ----------------------------------------------------------------------
def button_detect():
    global BtnChoix, BtnEnter, debug, channel, call, ferme_quit

    # ------------------------------------------------------------------
    # Detection des états-----------------------------------------------
    # ------------------------------------------------------------------

    # Call regarde s'il y a un changement d'état
    if (GPIO.input(EnterPin) == 1 and BtnEnter == False) or (GPIO.input(ChoicePin) == 1 and BtnChoix == False):
        call = True
    else:
        call = False

    # On mets dans la channel le numéro du bouton en question
    # et on ne le fait qu'une seule fois par appui
    if GPIO.input(EnterPin) == 1 and BtnEnter == False:
        if (debug): print "Enter"
        BtnEnter = True
        channel = EnterPin
    if GPIO.input(EnterPin) == 0:
        BtnEnter = False

    if GPIO.input(ChoicePin) == 1 and BtnChoix == False:
        if (debug): print "Choice"
        BtnChoix = True
        channel = ChoicePin
    if GPIO.input(ChoicePin) == 0:
        BtnChoix = False

    # ------------------------------------------------------------------
    # Actions-----------------------------------------------------------
    # ------------------------------------------------------------------
    global list_trans2, choix_trans2, choix_trans3, ouvert_trans1, ouvert_trans2, ouvert_trans3, list_menu, list_trans1, list_trans3, bouton_jeu1, bouton_jeu2, bouton_jeu3
    global go1, retour1, choix_menu, choix_trans1, ouvert_menu, ouvert_trans1, ouvert_lose1, list_lose1, recommencer1, choix_lose1, quit_losing1
    global go_cal1, retour_cal1, recommencer_cal1, choix_cal, list_cal, ouvert_cal, select_jeu1
    global go_cal2, retour_cal2, recommencer_cal2, select_jeu2
    global go_cal3, retour_cal3, recommencer_cal3, select_jeu3
    global go2, retour2, ouvert_win2, choix_win2, list_win2, recommencer2, quit_winning2, win2
    global go3, retour3, ouvert_win3, choix_win3, list_win3, recommencer3, quit_winning3, win3, jeu3, quitter_jeu3, ouvert_jeu3
    global PosX, PosY, obX, obY, obX2, obY2, obX3, obY3, obX4, obY4, obX5, obY5, obX6, obY6, obX7, obY7
    global Pion2, PosX2, PosY2, Hauteur, Largeur, x0, y0, x1, y1, jeu2, jeu2_niv1, jeu2_niv2, jeu2_niv3, jeu2_niv4
    global disc1, disc3, Pos_d1X, Pos_d1Y, Pos_d2X, Pos_d2Y

    # S'il y a eu un changement d'état sur un bouton et quon ne quitte pas
    if call and ferme_quit == 0:
        i = 0
        j = 0
        r = 0

        # Actions de menu principal
        if ouvert_menu == 1:
            if channel == ChoicePin:
                for i in range(len(list_menu)):
                    if list_menu[i] == 1:
                        list_menu[i] = 0
                        if i + 1 == 1:
                            list_menu[1] = 1
                            choix_menu = 1
                            break
                        elif i + 1 == 2:
                            list_menu[2] = 1
                            choix_menu = 2
                            break
                        else:
                            list_menu[0] = 1
                            choix_menu = 0
                            break
            if choix_menu == 0:
                bouton_jeu1.configure(bg='green')
                bouton_jeu2.configure(bg='deep pink')
                bouton_jeu3.configure(bg='deep pink')

            elif choix_menu == 1:
                bouton_jeu1.configure(bg='deep pink')
                bouton_jeu2.configure(bg='green')
                bouton_jeu3.configure(bg='deep pink')
            else:
                bouton_jeu1.configure(bg='deep pink')
                bouton_jeu2.configure(bg='deep pink')
                bouton_jeu3.configure(bg='green')

            if channel == EnterPin:
                if choix_menu == 0 and ouvert_menu == 1:
                    lancer_jeu1()
                if choix_menu == 1 and ouvert_menu == 1:
                    lancer_jeu2()
                if choix_menu == 2 and ouvert_menu == 1:
                    lancer_jeu3()

        # Actions de transition 1
        if ouvert_trans1 == 1:
            if channel == ChoicePin:
                for j in range(len(list_trans1)):
                    if list_trans1[j] == 1:
                        list_trans1[j] = 0
                        if j + 1 == 1:
                            list_trans1[1] = 1
                            choix_trans1 = 1
                            break
                        else:
                            list_trans1[0] = 1
                            choix_trans1 = 0
                            break

            if choix_trans1 == 0:
                go1.configure(bg='green')
                retour1.configure(bg='deep pink')
            else:
                retour1.configure(bg='green')
                go1.configure(bg='deep pink')

            if channel == EnterPin:
                if choix_trans1 == 0 and ouvert_trans1 == 1:
                    trans_cal1()
                elif choix_trans1 == 1 and ouvert_trans1 == 1:
                    back1()
                else:
                    back1()

        # Actions de calibration

        if ((ouvert_cal == 1) and (select_jeu1 == 1)):
            if channel == ChoicePin:
                for i in range(len(list_cal)):
                    if list_cal[i] == 1:
                        list_cal[i] = 0
                        if i + 1 == 1:
                            list_cal[1] = 1
                            choix_cal = 1
                            break
                        elif i + 1 == 2:
                            list_cal[2] = 1
                            choix_cal = 2
                            break
                        else:
                            list_cal[0] = 1
                            choix_cal = 0
                            break
            if choix_cal == 0:
                go_cal1.configure(bg='green')
                retour_cal1.configure(bg='deep pink')
                recommencer_cal1.configure(bg='deep pink')

            elif choix_cal == 1:
                go_cal1.configure(bg='deep pink')
                retour_cal1.configure(bg='green')
                recommencer_cal1.configure(bg='deep pink')
            else:
                go_cal1.configure(bg='deep pink')
                retour_cal1.configure(bg='deep pink')
                recommencer_cal1.configure(bg='green')

            if channel == EnterPin:
                if choix_cal == 0 and ouvert_cal == 1:
                    ready1()
                if choix_cal == 1 and ouvert_cal == 1:
                    back_calibration()
                if choix_cal == 2 and ouvert_cal == 1:
                    restart_calibration()

        if ((ouvert_cal == 1) and (select_jeu2 == 1)):
            if channel == ChoicePin:
                for i in range(len(list_cal)):
                    if list_cal[i] == 1:
                        list_cal[i] = 0
                        if i + 1 == 1:
                            list_cal[1] = 1
                            choix_cal = 1
                            break
                        elif i + 1 == 2:
                            list_cal[2] = 1
                            choix_cal = 2
                            break
                        else:
                            list_cal[0] = 1
                            choix_cal = 0
                            break
            if choix_cal == 0:
                go_cal2.configure(bg='green')
                retour_cal2.configure(bg='deep pink')
                recommencer_cal2.configure(bg='deep pink')

            elif choix_cal == 1:
                go_cal2.configure(bg='deep pink')
                retour_cal2.configure(bg='green')
                recommencer_cal2.configure(bg='deep pink')
            else:
                go_cal2.configure(bg='deep pink')
                retour_cal2.configure(bg='deep pink')
                recommencer_cal2.configure(bg='green')

            if channel == EnterPin:
                if choix_cal == 0 and ouvert_cal == 1:
                    ready2()
                if choix_cal == 1 and ouvert_cal == 1:
                    back_calibration()
                if choix_cal == 2 and ouvert_cal == 1:
                    restart_calibration()

        if ((ouvert_cal == 1) and (select_jeu3 == 1)):
            if channel == ChoicePin:
                for i in range(len(list_cal)):
                    if list_cal[i] == 1:
                        list_cal[i] = 0
                        if i + 1 == 1:
                            list_cal[1] = 1
                            choix_cal = 1
                            break
                        elif i + 1 == 2:
                            list_cal[2] = 1
                            choix_cal = 2
                            break
                        else:
                            list_cal[0] = 1
                            choix_cal = 0
                            break
            if choix_cal == 0:
                go_cal3.configure(bg='green')
                retour_cal3.configure(bg='deep pink')
                recommencer_cal3.configure(bg='deep pink')

            elif choix_cal == 1:
                go_cal3.configure(bg='deep pink')
                retour_cal3.configure(bg='green')
                recommencer_cal3.configure(bg='deep pink')
            else:
                go_cal3.configure(bg='deep pink')
                retour_cal3.configure(bg='deep pink')
                recommencer_cal3.configure(bg='green')

            if channel == EnterPin:
                if choix_cal == 0 and ouvert_cal == 1:
                    ready3()
                if choix_cal == 1 and ouvert_cal == 1:
                    back_calibration()
                if choix_cal == 2 and ouvert_cal == 1:
                    restart_calibration()

        # Actions de perdu 1
        if ouvert_lose1 == 1:
            if channel == ChoicePin:
                for r in range(len(list_lose1)):
                    if list_lose1[r] == 1:
                        list_lose1[r] = 0
                        if r + 1 == 1:
                            list_lose1[1] = 1
                            choix_lose1 = 1
                            break
                        else:
                            list_lose1[0] = 1
                            choix_lose1 = 0
                            break

            if choix_lose1 == 0:
                recommencer1.configure(bg='green')
                quit_losing1.configure(bg='deep pink')
            else:
                quit_losing1.configure(bg='green')
                recommencer1.configure(bg='deep pink')

            if channel == EnterPin:
                if choix_lose1 == 0:
                    recommencer_jeu1()
                elif choix_lose1 == 1:
                    quit_lose1()
                else:
                    quit_lose1()

        # Actions de transition 2
        if ouvert_trans2 == 1:
            if channel == ChoicePin:
                for j in range(len(list_trans2)):
                    if list_trans2[j] == 1:
                        list_trans2[j] = 0
                        if j + 1 == 1:
                            list_trans2[1] = 1
                            choix_trans2 = 1
                            break
                        else:
                            list_trans2[0] = 1
                            choix_trans2 = 0
                            break

            if choix_trans2 == 0:
                go2.configure(bg='green')
                retour2.configure(bg='deep pink')
            else:
                retour2.configure(bg='green')
                go2.configure(bg='deep pink')

            if channel == EnterPin:
                if choix_trans2 == 0 and ouvert_trans2 == 1:
                    trans_cal2()
                elif choix_trans2 == 1:
                    back2()
                else:
                    back2()

        # Actions de gagne 2
        if ouvert_win2 == 1:
            if channel == ChoicePin:
                for r in range(len(list_win2)):
                    if list_win2[r] == 1:
                        list_win2[r] = 0
                        if r + 1 == 1:
                            list_win2[1] = 1
                            choix_win2 = 1
                            break
                        else:
                            list_win2[0] = 1
                            choix_win2 = 0
                            break

            if choix_win2 == 0:
                recommencer2.configure(bg='green')
                quit_winning2.configure(bg='deep pink')
            else:
                quit_winning2.configure(bg='green')
                recommencer2.configure(bg='deep pink')

            if channel == EnterPin:
                if choix_win2 == 0:
                    recommencer_jeu2()
                elif choix_win2 == 1:
                    quit_win2()
                else:
                    quit_win2()

        # Actions de transition 3
        if ouvert_trans3 == 1:
            if channel == ChoicePin:
                for j in range(len(list_trans3)):
                    if list_trans3[j] == 1:
                        list_trans3[j] = 0
                        if j + 1 == 1:
                            list_trans3[1] = 1
                            choix_trans3 = 1
                            break
                        else:
                            list_trans3[0] = 1
                            choix_trans3 = 0
                            break

            if choix_trans3 == 0:
                go3.configure(bg='green')
                retour3.configure(bg='deep pink')
            else:
                retour3.configure(bg='green')
                go3.configure(bg='deep pink')

            if channel == EnterPin:
                if choix_trans3 == 0 and ouvert_trans3 == 1:
                    trans_cal3()
                elif choix_trans3 == 1:
                    back3()
                else:
                    back3()

        # Actions de gagne 3
        if ouvert_win3 == 1:
            if channel == ChoicePin:
                for r in range(len(list_win3)):
                    if list_win3[r] == 1:
                        list_win3[r] = 0
                        if r + 1 == 1:
                            list_win3[1] = 1
                            choix_win3 = 1
                            break
                        else:
                            list_win3[0] = 1
                            choix_win3 = 0
                            break

            if choix_win3 == 0:
                recommencer3.configure(bg='green')
                quit_winning3.configure(bg='deep pink')
            else:
                quit_winning3.configure(bg='green')
                recommencer3.configure(bg='deep pink')

            if channel == EnterPin:
                if choix_win3 == 0:
                    recommencer_jeu3()
                elif choix_win3 == 1:
                    quit_win3()
                else:
                    quit_win3()

        # Actions de jeu 1
        if ouvert_jeu1 == 1:
            if channel == EnterPin:
                quit_jeu1()

        # Actions de jeu 2
        if ouvert_jeu2 == 1:
            if channel == EnterPin:
                quit_jeu2()

        # Actions de jeu 3
        if ouvert_jeu3 == 1:
            if channel == EnterPin:
                quit_jeu3()

    # la fonction se rappelle automatiqement
    root.after(20, button_detect)



# ----------------------------------------------------------------------
def Clavier(event):
    global PosX, PosY, obX, obY, obX2, obY2, obX3, obY3, obX4, obY4, obX5, obY5, obX6, obY6, obX7, obY7
    touche = event.char

    if touche == 'd':
        PosX += Largeur / 100
    if touche == 'q':
        PosX -= Largeur / 100

    if touche == 'l':
        quit_jeu1()

    if PosX < 0:
        PosX = Largeur
    if PosX > Largeur:
        PosX = 0

    jeu1.coords(Pion, PosX - (Largeur / 50), PosY - (Largeur / 50), PosX + (Largeur / 50), PosY + (Largeur / 50))

    if PosX < 0:
        PosX = Largeur
    if PosX > Largeur:
        PosX = 0

    jeu1.coords(Pion, PosX - (Largeur / 50), PosY - (Largeur / 50), PosX + (Largeur / 50), PosY + (Largeur / 50))


def Clavier2(event2):
    global Pion2, PosX2, PosY2, Hauteur, Largeur, x0, y0, x1, y1, jeu2, jeu2_niv1, jeu2_niv2, jeu2_niv3, jeu2_niv4
    touche2 = event2.char

    if (PosX2 - (Largeur / (3.6)) < x0 < PosX2 - 10 and PosY2 - (Largeur / (3.6)) < y0 < PosY2 - 10 and PosX2 + (
            Largeur / (3.6)) > x1 > PosX2 + 10 and PosY2 + (Largeur / (3.6)) > y1 > PosY2 + 10):
        if touche2 == 'a':
            x0 -= 5
            y0 -= 5
            x1 += 5
            y1 += 5

        if touche2 == 'z':
            x0 += 5
            y0 += 5
            x1 -= 5
            y1 -= 5

    elif (x0 >= PosX2 - 10 and y0 >= PosY2 - 10 and x1 <= PosX2 + 10 and y1 <= PosY2 + 10):
        if touche2 == 'a':
            x0 -= 5
            y0 -= 5
            x1 += 5
            y1 += 5
        if touche2 == 'z':
            x0 += 0
            y0 += 0
            x1 -= 0
            y1 -= 0

    else:
        if touche2 == 'a':
            x0 += 0
            y0 += 0
            x1 -= 0
            y1 -= 0

        if touche2 == 'z':
            x0 += 5
            y0 += 5
            x1 -= 5
            y1 -= 5

    if touche2 == 'l':
        quit_jeu2()

    if jeu2_niv1 == 1:
        if ((PosX2 - (Largeur / (4))) < x0 < PosX2 - (Largeur / 5.2) and (PosY2 - (Largeur / (4))) < y0 < PosY2 - (
                Largeur / 5.2) and (PosX2 + (Largeur / (4))) > x1 > PosX2 + (Largeur / 5.2) and (
                PosY2 + (Largeur / (4))) > y1 > PosY2 + (Largeur / 5.2)):
            jeu2.itemconfig(Pion2, fill="green3", outline="green4")
        else:
            jeu2.itemconfig(Pion2, fill="lime green", outline="green4")

    if jeu2_niv2 == 1:
        if ((PosX2 - (Largeur / (4.2))) < x0 < PosX2 - (Largeur / 5) and (PosY2 - (Largeur / (4.2))) < y0 < PosY2 - (
                Largeur / 5) and (PosX2 + (Largeur / (4.2))) > x1 > PosX2 + (Largeur / 5) and (
                PosY2 + (Largeur / (4.2))) > y1 > PosY2 + (Largeur / 5)):
            jeu2.itemconfig(Pion2, fill="gold", outline="goldenrod2")
        else:
            jeu2.itemconfig(Pion2, fill="yellow", outline="goldenrod2")

    if jeu2_niv3 == 1:
        if ((PosX2 - (Largeur / (4.3))) < x0 < PosX2 - (Largeur / 4.8) and (PosY2 - (Largeur / (4.3))) < y0 < PosY2 - (
                Largeur / 4.8) and (PosX2 + (Largeur / (4.3))) > x1 > PosX2 + (Largeur / 4.8) and (
                PosY2 + (Largeur / (4.3))) > y1 > PosY2 + (Largeur / 4.8)):
            jeu2.itemconfig(Pion2, fill="red3", outline="red3")
        else:
            jeu2.itemconfig(Pion2, fill="red2", outline="red3")

    if jeu2_niv4 == 1:
        if ((PosX2 - (Largeur / (4.5))) < x0 < PosX2 - (Largeur / 4.8) and (PosY2 - (Largeur / (4.5))) < y0 < PosY2 - (
                Largeur / 4.8) and (PosX2 + (Largeur / (4.5))) > x1 > PosX2 + (Largeur / 4.8) and (
                PosY2 + (Largeur / (4.5))) > y1 > PosY2 + (Largeur / 4.8)):
            jeu2.itemconfig(Pion2, fill="gray14", outline="gray13")
        else:
            jeu2.itemconfig(Pion2, fill="gray15", outline="gray13")

    jeu2.coords(Pion2, x0, y0, x1, y1)


def Clavier3(event3):
    global jeu3, disc1, disc2, disc1_col, disc2_col
    touche3 = event3.char

    if touche3 == 'a':
        disc2_col = 0
        jeu3.itemconfig(disc2, fill="blue", outline="blue")

    if touche3 == 'z':
        disc2_col = 1
        jeu3.itemconfig(disc2, fill="red", outline="red")


# ======================================================================
#                               MENU
# ======================================================================
def lancer_menu():
    global debug, menu, bouton_jeu1, bouton_jeu2, bouton_jeu3, list_menu, ouvert_menu, choix_menu, select_jeu1, select_jeu2, select_jeu3

    if debug: print "lancer_menu"
    choix_menu = 0
    ouvert_menu = 1
    menu = Canvas(root, width=Largeur, height=Hauteur, bg='white')
    photo = PhotoImage(file=os.path.join(path, "normal.gif"))
    menu.create_image(Largeur / 10, Hauteur / 8, anchor=NW, image=photo)
    list_menu = [1, 0, 0]

    menu.focus_set()

    # menu.bind('<Key>',gerer_choix)

    select_jeu1 = 0
    select_jeu2 = 0
    select_jeu3 = 0

    bouton_jeu1 = Button(root, text='MINI JEU 1', command=lancer_jeu1, fg="white", bg="green",
                         activebackground="hot pink", activeforeground="white", font="Verdana 34 bold",
                         width=Largeur / 100)
    bouton_jeu1.pack()
    bouton_jeu1.place(width=(Largeur / 3.1), height=(Hauteur / 14.5), relx=0.6, rely=0.22)
    bouton_jeu2 = Button(root, text='MINI JEU 2', command=lancer_jeu2, fg="white", bg="deep pink",
                         activebackground="hot pink", activeforeground="white", font="Verdana 34 bold",
                         width=Largeur / 100)
    bouton_jeu2.pack()
    bouton_jeu2.place(width=(Largeur / 3.1), height=(Hauteur / 14.5), relx=0.6, rely=0.41)
    bouton_jeu3 = Button(root, text='MINI JEU 3', command=lancer_jeu3, fg="white", bg="deep pink",
                         activebackground="hot pink", activeforeground="white", font="Verdana 34 bold",
                         width=Largeur / 100)
    bouton_jeu3.pack()
    bouton_jeu3.place(width=(Largeur / 3.1), height=(Hauteur / 14.5), relx=0.6, rely=0.60)

    # bouton_quitter = Button(root, text='QUIT', command = quitter, fg="white", bg="white", font="verdana 34 bold", width=Largeur/100)
    # bouton_quitter.pack()
    # bouton_quitter.place(width=(Largeur/3.1), height=(Hauteur/14.5), relx=0, rely=0)

    button_detect()
    menu.pack(padx=0, pady=0)
    root.mainloop()


def quitter():
    ferme_quit = 1;
    root.destroy()


def lancer_jeu1():
    global debug, menu, bouton_jeu1, bouton_jeu2, bouton_jeu3, ouvert_menu
    if debug: print "lancer_jeu1"
    ouvert_menu = 0
    bouton_jeu1.destroy()
    bouton_jeu2.destroy()
    bouton_jeu3.destroy()
    menu.destroy()
    transition1()


def transition1():
    global debug, trans1, go1, retour1, ouvert_trans1, choix_trans1, list_trans1
    if debug: print "transition1"
    ouvert_trans1 = 1
    choix_trans1 = 0
    trans1 = Canvas(root, width=Largeur, height=Hauteur, bg='white')
    photo = PhotoImage(file=os.path.join(path, "screenjeu1.gif"))
    trans1.create_image(Largeur / 15, Hauteur / 8, anchor=NW, image=photo)
    list_trans1 = [1, 0]
    trans1.focus_set()

    # trans1.bind('<Key>',gerer_choix)

    go1 = Button(root, text="Suivant", command=trans_cal1, fg="white", bg="green", activebackground="hotpink",
                 activeforeground="white", font="Verdana 20 bold", width=Largeur / 130)
    go1.pack()
    go1.place(width=(Largeur / 5.7), height=(Hauteur / 18), relx=0.785, rely=0.90)
    retour1 = Button(root, text="Retour", command=back1, fg="white", bg="deep pink", activebackground="hotpink",
                     activeforeground="white", font="Verdana 20 bold", width=Largeur / 130)
    retour1.pack()
    retour1.place(width=(Largeur / 5.7), height=(Hauteur / 18), relx=0.04, rely=0.90)

    indic11 = Label(trans1, text="Le but de ce jeu est d'esquiver les blocs", bg="white", fg="hot pink",
                    font="Verdana 18 bold")
    indic11.pack()
    indic11.place(width=(Largeur / 2.5), height=(Hauteur / 20), relx=0.53, rely=0.15)

    indic12 = Label(trans1, text="qui tombent.                                             ", bg="white", fg="hot pink",
                    font="Verdana 18 bold")
    indic12.pack()
    indic12.place(width=(Largeur / 2.5), height=(Hauteur / 20), relx=0.53, rely=0.2)

    indic13 = Label(trans1, text="But : retravailler la coordination entre   ", bg="white", fg="deep sky blue",
                    font="Verdana 18 bold")
    indic13.pack()
    indic13.place(width=(Largeur / 2.5), height=(Hauteur / 20), relx=0.53, rely=0.3)

    indic14 = Label(trans1, text="un geste et un déplacement.                   ", bg="white", fg="deep sky blue",
                    font="Verdana 18 bold")
    indic14.pack()
    indic14.place(width=(Largeur / 2.5), height=(Hauteur / 20), relx=0.53, rely=0.35)

    trans1.pack()

    button_detect()
    root.mainloop()


def trans_cal1():
    global debug, trans1, go1, retour1, ouvert_trans1, select_jeu1
    if debug: print "trans_cal1"
    ouvert_trans1 = 0
    select_jeu1 = 1
    go1.destroy()
    retour1.destroy()
    trans1.destroy()
    calibration()


def demarrer_explication():
    if ouvert_cal == 1:
        exp_text1.configure(fg="black")
        exp_text2.configure(fg="black")
        exp_text3.configure(fg="black")
        exp_text4.configure(fg="black")
        root.after(1500, text1_color)


def text1_color():
    global exp_text1, cal_break
    if ouvert_cal == 1:
        exp_text1.configure(fg="deep sky blue")
        cal_break = 0
        root.after(1300, move_main1)


def move_main1():
    global cal, coord_mainX, coord_mainY, img_main
    if ouvert_cal == 1 and cal_break == 0:
        if coord_mainY < Hauteur - Hauteur / 2.6:
            coord_mainY = coord_mainY + 2
            cal.coords(img_main, coord_mainX, coord_mainY)
            root.after(1, move_main1)
        if coord_mainY >= Hauteur - Hauteur / 2.6:
            root.after(2000, text2_color)


def text2_color():
    global exp_text1, exp_text2
    if ouvert_cal == 1 and cal_break == 0:
        exp_text1.configure(fg="black")
        exp_text2.configure(fg="deep pink")
        root.after(1300, click_btn1)


def click_btn1():
    global cal, btn1X0, btn1X1, btn1Y0, btn1Y1, exp_bouton1, btn1_retour, btn1_pass

    if ouvert_cal == 1 and cal_break == 0:
        if btn1_pass == 0:
            if btn1_retour == 0:
                btn1X0 += 2
                btn1Y0 += 2
                btn1X1 -= 2
                btn1Y1 -= 2

            if btn1X0 == coord_btn1X - 8:
                btn1_retour = 1

            if btn1_retour == 1:
                if (btn1X0 != coord_btn1X - (Largeur / 55)):
                    btn1X0 -= 2
                    btn1Y0 -= 2
                    btn1X1 += 2
                    btn1Y1 += 2
                else:
                    btn1_pass = 1
            cal.coords(exp_bouton1, btn1X0, btn1Y0, btn1X1, btn1Y1)
            root.after(7, click_btn1)

        if btn1_pass == 1:
            root.after(2000, text34_color)


def text34_color():
    global exp_text2, exp_text3, exp_text4
    if ouvert_cal == 1 and cal_break == 0:
        exp_text2.configure(fg="black")
        exp_text3.configure(fg="SpringGreen4")
        exp_text4.configure(fg="SpringGreen4")
        root.after(1300, move_main2)


def move_main2():
    global cal, coord_mainX, coord_mainY, img_main
    if ouvert_cal == 1 and cal_break == 0:
        if coord_mainY > Hauteur - Hauteur / 1.4:
            coord_mainY = coord_mainY - 2

            cal.coords(img_main, coord_mainX, coord_mainY)

            root.after(4, move_main2)

        if coord_mainY <= Hauteur - Hauteur / 1.4:
            root.after(2000, text56_color)


def text56_color():
    global exp_text3, exp_text4, exp_text5, exp_text6
    if ouvert_cal == 1 and cal_break == 0:
        exp_text3.configure(fg="black")
        exp_text4.configure(fg="black")
        exp_text5.configure(fg="dark orange")
        exp_text6.configure(fg="dark orange")
        root.after(1300, click_btn2)


def click_btn2():
    global cal, btn2X0, btn2X1, btn2Y0, btn2Y1, exp_bouton2, btn2_retour
    if ouvert_cal == 1 and cal_break == 0:
        if btn2_pass == 0:
            if btn2_retour == 0:
                btn2X0 += 2
                btn2Y0 += 2
                btn2X1 -= 2
                btn2Y1 -= 2
                cal.coords(exp_bouton2, btn2X0, btn2Y0, btn2X1, btn2Y1)
                root.after(50, click_btn2)

            if btn2X0 == coord_btn2X - 8:
                btn2_retour = 1

            if btn2_retour == 1:
                if (btn2X0 != coord_btn2X - (Largeur / 55)):
                    btn2X0 -= 2
                    btn2Y0 -= 2
                    btn2X1 += 2
                    btn2Y1 += 2
                    cal.coords(exp_bouton2, btn2X0, btn2Y0, btn2X1, btn2Y1)
                    root.after(50, click_btn2)


def calibration():
    global debug, cal, choix_cal, list_cal, ouvert_cal
    global go_cal1, retour_cal1, recommencer_cal1
    global go_cal2, retour_cal2, recommencer_cal2
    global go_cal3, retour_cal3, recommencer_cal3
    global img_main
    global btn1X0, btn1X1, btn1Y0, btn1Y1, coord_btn1X, coord_btn1Y, exp_bouton1, btn1_retour, btn1_pass
    global btn2X0, btn2X1, btn2Y0, btn2Y1, coord_btn2X, coord_btn2Y, exp_bouton2, btn2_retour, btn2_pass
    global coord_mainX, coord_mainY
    global exp_text1, exp_text2, exp_text3, exp_text4, exp_text5, exp_text6
    global select_jeu1, select_jeu2, select_jeu3
    if debug: print "calibration1"
    choix_cal = 0
    ouvert_cal = 1
    cal = Canvas(root, width=Largeur, height=Hauteur, bg='white')
    list_cal = [1, 0, 0]
    cal.focus_set()

    photo_main = PhotoImage(file=os.path.join(path, "main.gif"))

    img_main = cal.create_image(Largeur - Largeur / 3, Hauteur - Hauteur / 1.8, anchor=NW, image=photo_main)
    coord_mainX = Largeur - Largeur / 3
    coord_mainY = Hauteur - Hauteur / 1.8

    coord_btn1X = Largeur / 2.2
    coord_btn1Y = Hauteur - Hauteur / 8
    btn1X0 = (coord_btn1X - (Largeur / 55))
    btn1X1 = (coord_btn1X + (Largeur / 55))
    btn1Y0 = (coord_btn1Y - (Largeur / 55))
    btn1Y1 = (coord_btn1Y + (Largeur / 55))
    btn1_retour = 0
    btn1_pass = 0

    coord_btn2X = Largeur / 2.6
    coord_btn2Y = Hauteur - Hauteur / 8
    btn2X0 = (coord_btn2X - (Largeur / 55))
    btn2X1 = (coord_btn2X + (Largeur / 55))
    btn2Y0 = (coord_btn2Y - (Largeur / 55))
    btn2Y1 = (coord_btn2Y + (Largeur / 55))
    btn2_retour = 0
    btn2_pass = 0

    coord_btn3X = Largeur / 3.2
    coord_btn3Y = Hauteur - Hauteur / 8

    coord_antenneX = Largeur / 2.3
    coord_antenneY = Hauteur - Hauteur / 5.5

    coord_borderX = Largeur / 9.7
    coord_borderY = Hauteur - Hauteur / 3.2

    coord_boiteX = Largeur / 8.78
    coord_boiteY = Hauteur - Hauteur / 3.4

    exp_titre = Label(cal, text="CALIBREZ LA REST !", fg="white", bg="deep pink", font="Verdana 30 bold")
    exp_titre.pack()
    exp_titre.place(relx=0.25, rely=0.05, width=Largeur / 2, height=Hauteur / 10)

    exp_antenne = cal.create_rectangle(coord_antenneX, coord_antenneY, coord_antenneX + (Largeur / 2),
                                       coord_antenneY + (Hauteur / 60), width=0, fill='gray65')
    boite_border = cal.create_rectangle(coord_borderX, coord_borderY, coord_borderX + (Largeur / 2.4),
                                        coord_borderY + (Hauteur / 3.5), width=0, fill='tan4')
    boite_boite = cal.create_rectangle(coord_boiteX, coord_boiteY, coord_boiteX + (Largeur / 2.535),
                                       coord_boiteY + (Hauteur / 4), width=0, fill='tan1')

    exp_bouton1 = cal.create_oval(btn1X0, btn1Y0, btn1X1, btn1Y1, width=1, fill='gray97', outline='black')
    exp_bouton2 = cal.create_oval(btn2X0, btn2Y0, btn2X1, btn2Y1, width=1, fill='gray97', outline='black')
    exp_bouton3 = cal.create_oval((coord_btn3X - (Largeur / 55)), (coord_btn3Y - (Largeur / 55)),
                                  (coord_btn3X + (Largeur / 55)), (coord_btn3Y + (Largeur / 55)), width=1,
                                  fill='gray97', outline='black')

    exp_text_btn1 = Label(cal, text="CALIBRATION", fg="tan4", bg="tan1", font="Verdana 8 bold")
    exp_text_btn1.pack()
    exp_text_btn1.place(relx=0.422, rely=0.81, width=Largeur / 15, height=Hauteur / 30)

    exp_text_btn2 = Label(cal, text="ENTER", fg="tan4", bg="tan1", font="Verdana 8 bold")
    exp_text_btn2.pack()
    exp_text_btn2.place(relx=0.352, rely=0.81, width=Largeur / 15, height=Hauteur / 30)

    exp_text_btn3 = Label(cal, text="CHOIX", fg="tan4", bg="tan1", font="Verdana 8 bold")
    exp_text_btn3.pack()
    exp_text_btn3.place(relx=0.279, rely=0.81, width=Largeur / 15, height=Hauteur / 30)

    exp_text1 = Label(cal, text="Approchez votre main de l'antenne", fg="black", bg="white", font="Verdana 16 bold")
    exp_text1.pack()
    exp_text1.place(relx=0.1, rely=0.25)

    exp_text2 = Label(cal, text="Appuyer sur le bouton CALIBRATION", fg="black", bg="white", font="Verdana 16 bold")
    exp_text2.pack()
    exp_text2.place(relx=0.1, rely=0.33)

    exp_text3 = Label(cal, text="Eloignez plus ou moins votre main de l'antenne", fg="black", bg="white",
                      font="Verdana 16 bold")
    exp_text3.pack()
    exp_text3.place(relx=0.1, rely=0.41)

    exp_text4 = Label(cal, text="en fonction des muscles sollicités", fg="black", bg="white", font="Verdana 16 bold")
    exp_text4.pack()
    exp_text4.place(relx=0.1, rely=0.44)

    exp_text5 = Label(cal, text="Sélectionner 'C'est Parti !' et appuyez sur le bouton", fg="black", bg="white",
                      font="Verdana 16 bold")
    exp_text5.pack()
    exp_text5.place(relx=0.1, rely=0.52)

    exp_text6 = Label(cal, text="ENTER pour commencer à jouer", fg="black", bg="white", font="Verdana 16 bold")
    exp_text6.pack()
    exp_text6.place(relx=0.1, rely=0.55)

    if select_jeu1 == 1:
        go_cal1 = Button(root, text="C'est parti !", command=ready1, fg="white", bg="green", activebackground="hotpink",
                         activeforeground="white", font="Verdana 10 bold")
        go_cal1.pack()
        go_cal1.place(width=(Largeur / 10), height=(Hauteur / 25), relx=0.85, rely=0.9)
        retour_cal1 = Button(root, text="Retour", command=back_calibration, fg="white", bg="deep pink",
                             activebackground="hotpink", activeforeground="white", font="Verdana 10 bold")
        retour_cal1.pack()
        retour_cal1.place(width=(Largeur / 10), height=(Hauteur / 25), relx=0.55, rely=0.9)
        recommencer_cal1 = Button(root, text="Recommencer", command=restart_calibration, fg="white", bg="deep pink",
                                  activebackground="hotpink", activeforeground="white", font="Verdana 10 bold")
        recommencer_cal1.pack()
        recommencer_cal1.place(width=(Largeur / 10), height=(Hauteur / 25), relx=0.70, rely=0.9)

    if select_jeu2 == 1:
        go_cal2 = Button(root, text="C'est parti !", command=ready2, fg="white", bg="green", activebackground="hotpink",
                         activeforeground="white", font="Verdana 10 bold")
        go_cal2.pack()
        go_cal2.place(width=(Largeur / 10), height=(Hauteur / 25), relx=0.85, rely=0.9)
        retour_cal2 = Button(root, text="Retour", command=back_calibration, fg="white", bg="deep pink",
                             activebackground="hotpink", activeforeground="white", font="Verdana 10 bold")
        retour_cal2.pack()
        retour_cal2.place(width=(Largeur / 10), height=(Hauteur / 25), relx=0.55, rely=0.9)
        recommencer_cal2 = Button(root, text="Recommencer", command=restart_calibration, fg="white", bg="deep pink",
                                  activebackground="hotpink", activeforeground="white", font="Verdana 10 bold")
        recommencer_cal2.pack()
        recommencer_cal2.place(width=(Largeur / 10), height=(Hauteur / 25), relx=0.70, rely=0.9)

    if select_jeu3 == 1:
        go_cal3 = Button(root, text="C'est parti !", command=ready2, fg="white", bg="green", activebackground="hotpink",
                         activeforeground="white", font="Verdana 10 bold")
        go_cal3.pack()
        go_cal3.place(width=(Largeur / 10), height=(Hauteur / 25), relx=0.85, rely=0.9)
        retour_cal3 = Button(root, text="Retour", command=back_calibration, fg="white", bg="deep pink",
                             activebackground="hotpink", activeforeground="white", font="Verdana 10 bold")
        retour_cal3.pack()
        retour_cal3.place(width=(Largeur / 10), height=(Hauteur / 25), relx=0.55, rely=0.9)
        recommencer_cal3 = Button(root, text="Recommencer", command=restart_calibration, fg="white", bg="deep pink",
                                  activebackground="hotpink", activeforeground="white", font="Verdana 10 bold")
        recommencer_cal3.pack()
        recommencer_cal3.place(width=(Largeur / 10), height=(Hauteur / 25), relx=0.70, rely=0.9)

    demarrer_explication()

    cal.pack()

    button_detect()

    root.mainloop()


def lancer_jeu2():
    global debug, menu, bouton_jeu1, bouton_jeu2, bouton_jeu3, ouvert_menu
    if debug: print "lancer_jeu2"
    ouvert_menu = 0
    bouton_jeu1.destroy()
    bouton_jeu2.destroy()
    bouton_jeu3.destroy()
    menu.destroy()
    transition2()


def transition2():
    global debug, trans2, go2, retour2, list_trans2, ouvert_trans2, choix_trans2
    if debug: print "transition2"
    ouvert_trans2 = 1
    choix_trans2 = 0
    trans2 = Canvas(root, width=Largeur, height=Hauteur, bg='white')
    photo = PhotoImage(file=os.path.join(path, "jeu2.gif"))
    trans2.create_image(Largeur / 15, Hauteur / 8, anchor=NW, image=photo)
    list_trans2 = [1, 0]

    trans2.focus_set()
    # trans2.bind('<Key>',gerer_choix2)

    go2 = Button(root, text="Suivant", command=trans_cal2, fg="white", bg="green", activebackground="hotpink",
                 activeforeground="white", font="Verdana 20 bold", width=Largeur / 120)
    go2.pack()
    go2.place(width=(Largeur / 5.7), height=(Hauteur / 18), relx=0.785, rely=0.90)
    retour2 = Button(root, text="Retour", command=back2, fg="white", bg="deep pink", activebackground="hotpink",
                     activeforeground="white", font="Verdana 20 bold", width=Largeur / 120)
    retour2.pack()
    retour2.place(width=(Largeur / 5.7), height=(Hauteur / 18), relx=0.04, rely=0.90)

    indic21 = Label(trans2, text="Le but  de ce jeu est de modifier la taille", bg="white", fg="hot pink",
                    font="Verdana 18 bold")
    indic21.pack()
    indic21.place(width=(Largeur / 2.5), height=(Hauteur / 20), relx=0.53, rely=0.15)

    indic22 = Label(trans2, text="du disque centrale  pour rentrer dans  la", bg="white", fg="hot pink",
                    font="Verdana 18 bold")
    indic22.pack()
    indic22.place(width=(Largeur / 2.5), height=(Hauteur / 20), relx=0.53, rely=0.2)

    indic23 = Label(trans2, text="zone grisée  et  maintenir  cette position", bg="white", fg="hot pink",
                    font="Verdana 18 bold")
    indic23.pack()
    indic23.place(width=(Largeur / 2.5), height=(Hauteur / 20), relx=0.53, rely=0.25)

    indic24 = Label(trans2, text="jusqu'à que  le compteur atteigne 30.     ", bg="white", fg="hot pink",
                    font="Verdana 18 bold")
    indic24.pack()
    indic24.place(width=(Largeur / 2.5), height=(Hauteur / 20), relx=0.53, rely=0.3)

    indic25 = Label(trans2, text="But : retravailler la stabilité et éviter les ", bg="white", fg="deep sky blue",
                    font="Verdana 18 bold")
    indic25.pack()
    indic25.place(width=(Largeur / 2.5), height=(Hauteur / 20), relx=0.53, rely=0.4)

    indic26 = Label(trans2, text="tremblements.                                           ", bg="white",
                    fg="deep sky blue", font="Verdana 18 bold")
    indic26.pack()
    indic26.place(width=(Largeur / 2.5), height=(Hauteur / 20), relx=0.53, rely=0.45)

    trans2.pack()

    button_detect()

    root.mainloop()


def trans_cal2():
    global debug, trans2, go2, retour2, ouvert_trans2, select_jeu2
    if debug: print "trans_cal2"
    ouvert_trans2 = 0
    select_jeu2 = 1
    go2.destroy()
    retour2.destroy()
    trans2.destroy()
    calibration()


def lancer_jeu3():
    global debug, menu, bouton_jeu1, bouton_jeu2, bouton_jeu3, ouvert_menu
    if debug: print "lancer_jeu3"
    ouvert_menu = 0
    bouton_jeu1.destroy()
    bouton_jeu2.destroy()
    bouton_jeu3.destroy()
    menu.destroy()
    transition3()


def transition3():
    global debug, trans3, go3, retour3, ouvert_trans3, choix_trans3, list_trans3
    if debug: print "transition3"
    ouvert_trans3 = 1
    choix_trans3 = 0
    trans3 = Canvas(root, width=Largeur, height=Hauteur, bg='white')
    photo = PhotoImage(file=os.path.join(path, "screen3_jeu3_40.gif"))
    trans3.create_image(Largeur / 15, Hauteur / 8, anchor=NW, image=photo)
    list_trans3 = [1, 0]
    trans3.focus_set()

    # trans1.bind('<Key>',gerer_choix)

    go3 = Button(root, text="Suivant", command=trans_cal3, fg="white", bg="green", activebackground="hotpink",
                 activeforeground="white", font="Verdana 20 bold", width=Largeur / 130)
    go3.pack()
    go3.place(width=(Largeur / 5.7), height=(Hauteur / 18), relx=0.785, rely=0.90)
    retour3 = Button(root, text="Retour", command=back3, fg="white", bg="deep pink", activebackground="hotpink",
                     activeforeground="white", font="Verdana 20 bold", width=Largeur / 130)
    retour3.pack()
    retour3.place(width=(Largeur / 5.7), height=(Hauteur / 18), relx=0.04, rely=0.90)

    indic31 = Label(trans3, text="Le but de ce jeu  est  de réussir 3 fois de", bg="white", fg="hot pink",
                    font="Verdana 18 bold")
    indic31.pack()
    indic31.place(width=(Largeur / 2.5), height=(Hauteur / 20), relx=0.53, rely=0.15)

    indic32 = Label(trans3, text="suite à coordonner son mouvement avec", bg="white", fg="hot pink",
                    font="Verdana 18 bold")
    indic32.pack()
    indic32.place(width=(Largeur / 2.5), height=(Hauteur / 20), relx=0.53, rely=0.2)

    indic33 = Label(trans3, text="le disque qui change de couleur.              ", bg="white", fg="hot pink",
                    font="Verdana 18 bold")
    indic33.pack()
    indic33.place(width=(Largeur / 2.5), height=(Hauteur / 20), relx=0.53, rely=0.25)

    indic34 = Label(trans3, text="But  :  retravailler  le  synchronisation     ", bg="white", fg="deep sky blue",
                    font="Verdana 18 bold")
    indic34.pack()
    indic34.place(width=(Largeur / 2.5), height=(Hauteur / 20), relx=0.53, rely=0.35)

    indic35 = Label(trans3, text="entre un geste et un timing précis.          ", bg="white", fg="deep sky blue",
                    font="Verdana 18 bold")
    indic35.pack()
    indic35.place(width=(Largeur / 2.5), height=(Hauteur / 20), relx=0.53, rely=0.40)

    trans3.pack()

    button_detect()
    root.mainloop()


def trans_cal3():
    global debug, trans3, go3, retour3, ouvert_trans3, select_jeu3
    if debug: print "trans_cal3"
    ouvert_trans3 = 0
    select_jeu3 = 1
    go3.destroy()
    retour3.destroy()
    trans3.destroy()
    calibration()


def back1():
    global debug, trans1, go1, retour1, ouvert_trans1
    if debug: print "back1"
    ouvert_trans1 = 0
    go1.destroy()
    retour1.destroy()
    trans1.destroy()
    lancer_menu()


def back_calibration():
    global debug, cal, ouvert_cal, select_jeu1, select_jeu2, select_jeu3
    global go_cal1, retour_cal1, recommencer_cal1
    global go_cal2, retour_cal2, recommencer_cal2
    global go_cal3, retour_cal3, recommencer_cal3
    if debug: print "back_calibration"
    ouvert_cal = 0

    if select_jeu1 == 1:
        go_cal1.destroy()
        recommencer_cal1.destroy()
        retour_cal1.destroy()
        cal.destroy()
        transition1()

    if select_jeu2 == 1:
        go_cal2.destroy()
        recommencer_cal2.destroy()
        retour_cal2.destroy()
        cal.destroy()
        transition2()

    if select_jeu3 == 1:
        go_cal3.destroy()
        recommencer_cal3.destroy()
        retour_cal3.destroy()
        cal.destroy()
        transition3()


def restart_calibration():
    global select_jeu1, select_jeu2, select_jeu3, cal
    global go_cal1, retour_cal1, recommencer_cal1
    global go_cal2, retour_cal2, recommencer_cal2
    global go_cal3, retour_cal3, recommencer_cal3
    global cal_break

    cal_break = 1

    if select_jeu1 == 1:
        go_cal1.destroy()
        retour_cal1.destroy()
        recommencer_cal1.destroy()
        cal.destroy()
        calibration()

        if select_jeu2 == 1:
            go_cal2.destroy()
            retour_cal2.destroy()
            recommencer_cal2.destroy()
            cal.destroy()
            calibration()

        if select_jeu3 == 1:
            go_cal3.destroy()
            retour_cal3.destroy()
            recommencer_cal3.destroy()
            cal.destroy()
            calibration()


def back2():
    global debug, trans2, go2, retour2, ouvert_trans2
    if debug: print "back2"
    ouvert_trans2 = 0
    go2.destroy()
    retour2.destroy()
    trans2.destroy()
    lancer_menu()


def back3():
    global debug, trans3, go3, retour3, ouvert_trans3
    if debug: print "back3"
    ouvert_trans3 = 0
    go3.destroy()
    retour3.destroy()
    trans3.destroy()
    lancer_menu()


# ======================================================================
#                           CALIBRATION
# ======================================================================
def ready1():
    global debug, cal, go_cal1, retour_cal1, ouvert_cal, MAX, freq
    if debug: print "ready1"
    if freq == -1:
        print "Freq = -1 : ARDUINO NOT CONNECTED"
        quitter()

    MAX = 2000
    # ~ while MAX>=2000 or MAX<100:
    MAX = freq
    if debug: print "MAX = ", MAX

    ouvert_cal = 0
    go_cal1.destroy()
    recommencer_cal1.destroy()
    retour_cal1.destroy()
    cal.destroy()
    mjeu1()


def ready2():
    global debug, cal, go_cal2, retour_cal2, ouvert_cal, MAX, freq
    if debug: print "ready2"
    if freq == -1:
        print "Freq = -1 : ARDUINO NOT CONNECTED"
        quitter()

    # Max c'est la valeur qu'on enregistre quand la main est la plus loin
    MAX = 2000
    # ~ while MAX>=2000 or MAX<100:
    MAX = freq
    print "MAX"
    print MAX
    if debug: print "MAX = ", MAX

    ouvert_cal = 0
    go_cal2.destroy()
    retour_cal2.destroy()
    cal.destroy()
    mjeu2()


def ready3():
    global debug, cal, go_cal3, retour_cal3, ouvert_cal, MAX, freq
    if debug: print "ready3"
    if freq == -1:
        print "Freq = -1 : ARDUINO NOT CONNECTED"
        quitter()

    # Max c'est la valeur qu'on enregistre quand la main est la plus loin
    MAX = 2000
    # ~ while MAX>=2000 or MAX<100:
    MAX = freq
    if debug: print "MAX = ", MAX

    ouvert_cal = 0
    go_cal3.destroy()
    retour_cal3.destroy()
    cal.destroy()
    mjeu3()


# ======================================================================
#                               JEUX
# ======================================================================

# ----------------------------------------------------------------------
#                               JEU 1
# ----------------------------------------------------------------------
def mjeu1():
    global debug, obX, obY, obX2, obY2, obX3, obY3, obX4, obY4, obX5, obY5, obX6, obY6, obX7, obY7, obX8, obY8, obX9, obY9, counter, Hauteur, Largeur, PosX, PosY, jeu1, obstacle, obstacle2, obstacle3, obstacle4, obstacle5, obstacle6, obstacle7, obstacle8, obstacle9, Barre, Score, Points, Pion, jeu1, quitter_jeu1, var, ouvert_jeu1, MAX
    if debug: print "mjeu1"
    ouvert_jeu1 = 1
    PosX = 0 + (Largeur / 2)
    PosY = Hauteur - (Hauteur / 5)
    obX = random.randint(0 + (Largeur / 5), Largeur - (Largeur / 5))
    obY = 0 - Hauteur / 4
    obX2 = random.randint(0 + (Largeur / 5), Largeur - (Largeur / 5))
    obY2 = 0 - 1.8 * (Hauteur / 4)
    obX3 = random.randint(0 + (Largeur / 5), Largeur - (Largeur / 5))
    obY3 = 0 - 2.6 * (Hauteur / 4)
    obX4 = random.randint(0 + (Largeur / 5), Largeur - (Largeur / 5))
    obY4 = 0 - 3.4 * (Hauteur / 4)
    obX5 = random.randint(0 + (Largeur / 5), Largeur - (Largeur / 5))
    obY5 = 0 - 4.2 * (Hauteur / 4)
    obX6 = random.randint(0 + (Largeur / 5), Largeur - (Largeur / 5))
    obY6 = 0 - 5 * (Hauteur / 4)
    obX7 = random.randint(0 + (Largeur / 5), Largeur - (Largeur / 5))
    obY7 = 0 - 5.8 * (Hauteur / 4)
    obX8 = random.randint(0 + (Largeur / 5), Largeur - (Largeur / 5))
    obY8 = 0 - 6.6 * (Hauteur / 4)
    obX9 = random.randint(0 + (Largeur / 5), Largeur - (Largeur / 5))
    obY9 = 0 - 7.4 * (Hauteur / 4)

    counter = 0

    var = IntVar()

    jeu1 = Canvas(root, width=Largeur, height=Hauteur, bg='white')

    photo = PhotoImage(file=os.path.join(path, "normal.gif"))
    jeu1.create_image(Largeur / 3.2, Hauteur / 8, anchor=NW, image=photo)

    Barre = Label(jeu1, text="REST", fg="deep pink", bg="deep pink", font="Verdana 22 bold")
    Score = Label(jeu1, text="SCORE :", fg="snow", bg="deep pink", font="Verdana 22 bold")
    Points = Label(jeu1, textvariable=var, fg="snow", bg="deep pink", font="Verdana 22 bold")
    Pion = jeu1.create_oval((PosX - (Largeur / 50)), (PosY - (Largeur / 50)), (PosX + (Largeur / 50)),
                            (PosY + (Largeur / 50)), width=2, fill='red')
    quitter_jeu1 = Button(root, text='QUITTER LE JEU', command=quit_jeu1, fg="white", bg="green",
                          activeforeground="white", activebackground="hot pink", font="Verdana 14 bold")

    # Gestion des obstacles descendants
    obstacle = jeu1.create_rectangle(obX - (Largeur / 40), obY - (Largeur / 40), obX + (Largeur / 40),
                                     obY + (Largeur / 40), width=2, fill='purple')
    obstacle2 = jeu1.create_rectangle(obX2 - (Largeur / 20), obY2 - (Largeur / 20), obX2 + (Largeur / 20),
                                      obY2 + (Largeur / 20), width=2, fill='RoyalBlue3')
    obstacle3 = jeu1.create_rectangle(obX3 - (Largeur / 20), obY3 - (Largeur / 20), obX3 + (Largeur / 20),
                                      obY3 + (Largeur / 20), width=2, fill='DeepskyBlue2')
    obstacle4 = jeu1.create_rectangle(obX4 - (Largeur / 20), obY4 - (Largeur / 20), obX4 + (Largeur / 20),
                                      obY4 + (Largeur / 20), width=2, fill='green')
    obstacle5 = jeu1.create_rectangle(obX5 - (Largeur / 20), obY5 - (Largeur / 20), obX5 + (Largeur / 20),
                                      obY5 + (Largeur / 20), width=2, fill='yellow')
    obstacle6 = jeu1.create_rectangle(obX6 - (Largeur / 20), obY6 - (Largeur / 20), obX6 + (Largeur / 20),
                                      obY6 + (Largeur / 20), width=2, fill='orange')
    obstacle7 = jeu1.create_rectangle(obX7 - (Largeur / 20), obY7 - (Largeur / 20), obX7 + (Largeur / 20),
                                      obY7 + (Largeur / 20), width=2, fill='red')
    obstacle8 = jeu1.create_rectangle(obX8 - (Largeur / 20), obY8 - (Largeur / 20), obX8 + (Largeur / 20),
                                      obY8 + (Largeur / 20), width=2, fill='VioletRed1')
    obstacle9 = jeu1.create_rectangle(obX9 - (Largeur / 20), obY9 - (Largeur / 20), obX9 + (Largeur / 20),
                                      obY9 + (Largeur / 20), width=2, fill='magenta3')
    anime()
    jeu1.focus_set()

    # Je laisse le controle clavier pour débugger
    jeu1.bind('<Key>', Clavier)

    Barre.pack()
    Barre.place(width=Largeur, height=(Hauteur / 20), relx=0, rely=0.95)
    Score.pack()
    Score.place(width=(Largeur / 7), height=(Hauteur / 20), relx=0.42, rely=0.951)
    Points.pack()
    Points.place(width=(Largeur / 24), height=(Hauteur / 20), relx=0.54, rely=0.951)

    quitter_jeu1.pack()
    quitter_jeu1.place(width=(Largeur / 7), height=(Hauteur / 20), relx=0.859, rely=0.950)
    jeu1.pack(padx=0, pady=0)

    button_detect()
    root.mainloop()


def collision():
    global debug, jeu1, quitter_jeu1, ouvert_jeu1
    if debug: print "collision"
    ouvert_jeu1 = 0

    quitter_jeu1.destroy()
    jeu1.destroy()
    losing1()


def anime():
    global debug, obX, obY, obX2, obY2, obX3, obY3, obX4, obY4, obX5, obY5, obX6, obY6, obX7, obY7, obX8, obY8, obX9, obY9, counter, Hauteur, Largeur, PosX, PosY, MAX, freq

    if ouvert_jeu1 == 1:
        if debug: print "anime"

        # Lecture frequence -> position
        if freq < MAX:
            PosX = freq * Largeur / MAX

        if PosX < 0:
            PosX = Largeur
        if PosX > Largeur:
            PosX = 0
        jeu1.coords(Pion, PosX - (Largeur / 50), PosY - (Largeur / 50), PosX + (Largeur / 50), PosY + (Largeur / 50))

        if obY < Hauteur + 20:
            if counter < 30:
                obY += Hauteur / 80
            elif (30 <= counter <= 59):
                obY += Hauteur / 60
            elif (60 <= counter <= 89):
                obY += Hauteur / 40
            else:
                obY += Hauteur / 20

            jeu1.coords(obstacle, obX - (Largeur / 35), obY - (Largeur / 35), obX + (Largeur / 35),
                        obY + (Largeur / 35))

            if obY >= Hauteur + 20:
                obY = 0 - 3 * (Hauteur / 4)
                obX = random.randint(0 + (Largeur / 18), Largeur - (Largeur / 18))
                counter = counter + 1

        if obY2 < Hauteur + 20:
            if counter < 30:
                obY2 += Hauteur / 80
            elif (30 <= counter <= 59):
                obY2 += Hauteur / 60
            elif (60 <= counter <= 89):
                obY2 += Hauteur / 40
            else:
                obY2 += Hauteur / 20
            jeu1.coords(obstacle2, obX2 - (Largeur / 35), obY2 - (Largeur / 35), obX2 + (Largeur / 35),
                        obY2 + (Largeur / 35))

            if obY2 >= Hauteur + 20:
                obY2 = 0 - 3 * (Hauteur / 4)
                obX2 = random.randint(0 + (Largeur / 18), Largeur - (Largeur / 18))
                counter = counter + 1

        if obY3 < Hauteur + 20:
            if counter < 30:
                obY3 += Hauteur / 80
            elif (30 <= counter <= 59):
                obY3 += Hauteur / 60
            elif (60 <= counter <= 89):
                obY3 += Hauteur / 40
            else:
                obY3 += Hauteur / 20
            jeu1.coords(obstacle3, obX3 - (Largeur / 35), obY3 - (Largeur / 35), obX3 + (Largeur / 35),
                        obY3 + (Largeur / 35))

            if obY3 >= Hauteur + 20:
                obY3 = 0 - 3 * (Hauteur / 4)
                obX3 = random.randint(0 + (Largeur / 18), Largeur - (Largeur / 18))
                counter = counter + 1

        if obY4 < Hauteur + 20:
            if counter < 30:
                obY4 += Hauteur / 80
            elif (30 <= counter <= 59):
                obY4 += Hauteur / 60
            elif (60 <= counter <= 89):
                obY4 += Hauteur / 40
            else:
                obY4 += Hauteur / 20
            jeu1.coords(obstacle4, obX4 - (Largeur / 35), obY4 - (Largeur / 35), obX4 + (Largeur / 35),
                        obY4 + (Largeur / 35))

            if obY4 >= Hauteur + 20:
                obY4 = 0 - 3 * (Hauteur / 4)
                obX4 = random.randint(0 + (Largeur / 18), Largeur - (Largeur / 18))
                counter = counter + 1

        if obY5 < Hauteur + 20:
            if counter < 30:
                obY5 += Hauteur / 80
            elif (30 <= counter <= 59):
                obY5 += Hauteur / 60
            elif (60 <= counter <= 89):
                obY5 += Hauteur / 40
            else:
                obY5 += Hauteur / 20
            jeu1.coords(obstacle5, obX5 - (Largeur / 35), obY5 - (Largeur / 35), obX5 + (Largeur / 35),
                        obY5 + (Largeur / 35))

            if obY5 >= Hauteur + 20:
                obY5 = 0 - 3 * (Hauteur / 4)
                obX5 = random.randint(0 + (Largeur / 18), Largeur - (Largeur / 18))
                counter = counter + 1

        if obY6 < Hauteur + 20:
            if counter < 30:
                obY6 += Hauteur / 80
            elif (30 <= counter <= 59):
                obY6 += Hauteur / 60
            elif (60 <= counter <= 89):
                obY6 += Hauteur / 40
            else:
                obY6 += Hauteur / 20
            jeu1.coords(obstacle6, obX6 - (Largeur / 35), obY6 - (Largeur / 35), obX6 + (Largeur / 35),
                        obY6 + (Largeur / 35))

            if obY6 >= Hauteur + 20:
                obY6 = 0 - 3 * (Hauteur / 4)
                obX6 = random.randint(0 + (Largeur / 18), Largeur - (Largeur / 18))
                counter = counter + 1

        if obY7 < Hauteur + 20:
            if counter < 30:
                obY7 += Hauteur / 80
            elif (30 <= counter <= 59):
                obY7 += Hauteur / 60
            elif (60 <= counter <= 89):
                obY7 += Hauteur / 40
            else:
                obY7 += Hauteur / 20
            jeu1.coords(obstacle7, obX7 - (Largeur / 35), obY7 - (Largeur / 35), obX7 + (Largeur / 35),
                        obY7 + (Largeur / 35))

            if obY7 >= Hauteur + 20:
                obY7 = 0 - 3 * (Hauteur / 4)
                obX7 = random.randint(0 + (Largeur / 18), Largeur - (Largeur / 18))
                counter = counter + 1

        if obY8 < Hauteur + 20:
            if counter < 30:
                obY8 += Hauteur / 80
            elif (30 <= counter <= 59):
                obY8 += Hauteur / 60
            elif (60 <= counter <= 89):
                obY8 += Hauteur / 40
            else:
                obY8 += Hauteur / 20
            jeu1.coords(obstacle8, obX8 - (Largeur / 35), obY8 - (Largeur / 35), obX8 + (Largeur / 35),
                        obY8 + (Largeur / 35))

            if obY8 >= Hauteur + 20:
                obY8 = 0 - 3 * (Hauteur / 4)
                obX8 = random.randint(0 + (Largeur / 18), Largeur - (Largeur / 18))
                counter = counter + 1

        if obY9 < Hauteur + 20:
            if counter < 30:
                obY9 += Hauteur / 80
            elif (30 <= counter <= 59):
                obY9 += Hauteur / 60
            elif (60 <= counter <= 89):
                obY9 += Hauteur / 40
            else:
                obY9 += Hauteur / 20
            jeu1.coords(obstacle9, obX9 - (Largeur / 35), obY9 - (Largeur / 35), obX9 + (Largeur / 35),
                        obY9 + (Largeur / 35))

            if obY9 >= Hauteur + 20:
                obY9 = 0 - 3 * (Hauteur / 4)
                obX9 = random.randint(0 + (Largeur / 18), Largeur - (Largeur / 18))
                counter = counter + 1

        if (obY - (Largeur / 22.2) <= PosY <= obY + (Largeur / 22.2)) and (
                obX - (Largeur / 22.2) <= PosX <= obX + (Largeur / 22.2)):
            time.sleep(1)
            collision()

        elif (obY2 - (Largeur / 22.2) <= PosY <= obY2 + (Largeur / 22.2)) and (
                obX2 - (Largeur / 22.2) <= PosX <= obX2 + (Largeur / 22.2)):
            time.sleep(1)
            collision()

        elif (obY3 - (Largeur / 22.2) <= PosY <= obY3 + (Largeur / 22.2)) and (
                obX3 - (Largeur / 22.2) <= PosX <= obX3 + (Largeur / 22.2)):
            time.sleep(1)
            collision()

        elif (obY4 - (Largeur / 22.2) <= PosY <= obY4 + (Largeur / 22.2)) and (
                obX4 - (Largeur / 22.2) <= PosX <= obX4 + (Largeur / 22.2)):
            time.sleep(1)
            collision()

        elif (obY5 - (Largeur / 22.2) <= PosY <= obY5 + (Largeur / 22.2)) and (
                obX5 - (Largeur / 22.2) <= PosX <= obX5 + (Largeur / 22.2)):
            time.sleep(1)
            collision()

        elif (obY6 - (Largeur / 22.2) <= PosY <= obY6 + (Largeur / 22.2)) and (
                obX6 - (Largeur / 22.2) <= PosX <= obX6 + (Largeur / 22.2)):
            time.sleep(1)
            collision()

        elif (obY7 - (Largeur / 22.2) <= PosY <= obY7 + (Largeur / 22.2)) and (
                obX7 - (Largeur / 22.2) <= PosX <= obX7 + (Largeur / 22.2)):
            time.sleep(1)
            collision()

        elif (obY8 - (Largeur / 22.2) <= PosY <= obY8 + (Largeur / 22.2)) and (
                obX8 - (Largeur / 22.2) <= PosX <= obX8 + (Largeur / 22.2)):
            time.sleep(1)
            collision()

        elif (obY9 - (Largeur / 22.2) <= PosY <= obY9 + (Largeur / 22.2)) and (
                obX9 - (Largeur / 22.2) <= PosX <= obX9 + (Largeur / 22.2)):
            time.sleep(1)
            collision()

        var.set(counter)

        root.after(45, anime)


def losing1():
    global debug, lose1, recommencer1, quit_losing1, var, ouvert_lose1, list_lose1, choix_lose1
    if debug: print "losing1"

    ouvert_lose1 = 1
    list_lose1 = [1, 0]
    choix_lose1 = 0
    lose1 = Canvas(root, width=Largeur, height=Hauteur, bg='white')
    lose1.focus_set()

    # lose1.bind('<Key>',gerer_choix)

    perdu = Label(lose1, text="Mince alors !", fg="deep pink", bg="white", font="Verdana 60 bold")
    perdu.pack()
    perdu.place(width=(Largeur / 2), height=(Hauteur / 12), relx=0.26, rely=0.1)
    perdu2 = Label(lose1, text="Que faire ?", fg="hot pink", bg="white", font="Verdana 40 bold")
    perdu2.pack()
    perdu2.place(width=(Largeur / 3), height=(Hauteur / 12), relx=0.334, rely=0.23)
    Points_lose = Label(lose1, textvariable=var, fg="deep pink", bg="white", font="Verdana 40 bold")
    Points_lose.pack()
    Points_lose.place(width=(Largeur / 9), height=(Hauteur / 15), relx=0.545, rely=0.39)
    Score_lose = Label(lose1, text="SCORE :", fg="deep pink", bg="white", font="Verdana 40 bold")
    Score_lose.pack()
    Score_lose.place(width=(Largeur / 5), height=(Hauteur / 15), relx=0.365, rely=0.39)

    recommencer1 = Button(root, text='RECOMMENCER', command=recommencer_jeu1, font="Verdana 20 bold", fg="white",
                          bg="green", activebackground="hot pink", activeforeground="white", width=Largeur / 60)
    recommencer1.pack()
    recommencer1.place(width=(Largeur / 3), height=(Largeur / 21), relx=0.34, rely=0.6)
    quit_losing1 = Button(root, text='QUITTER', command=quit_lose1, fg="white", bg="deep pink",
                          activebackground="hot pink", activeforeground="white", font="Verdana 20 bold",
                          width=Largeur / 60)
    quit_losing1.pack()
    quit_losing1.place(width=(Largeur / 3), height=(Largeur / 21), relx=0.34, rely=0.7)
    lose1.pack(padx=0, pady=0)

    button_detect()
    root.mainloop()


def quit_lose1():
    global debug, lose1, recommencer1, quit_losing1, ouvert_lose1
    if debug: print "quit_lose1"
    ouvert_lose1 = 0
    recommencer1.destroy()
    quit_losing1.destroy()
    lose1.destroy()
    lancer_menu()


def recommencer_jeu1():
    global debug, lose1, recommencer1, quit_losing1, ouvert_lose1
    if debug: print "recommencer_jeu1"
    ouvert_lose1 = 0
    recommencer1.destroy()
    quit_losing1.destroy()
    lose1.destroy()
    mjeu1()


def quit_jeu1():
    global debug, jeu1, quitter_jeu1, ouvert_jeu1
    if debug: print "quit_jeu1"
    ouvert_jeu1 = 0
    quitter_jeu1.destroy()
    jeu1.destroy()
    lancer_menu()


# ----------------------------------------------------------------------
#                               JEU 2
# ----------------------------------------------------------------------
def mjeu2():
    global debug, jeu2, minmax, quitter_jeu2, ouvert_jeu2, x0, y0, x1, y1, PosX2, PosY2, Pion2, Pion3, Pion4, Pion5, Pion6, jeu2, ouvert_jeu2, var2, counter_time, Hauteur, Largeur, Maintient, jeu2_niv1, jeu2_niv2, jeu2_niv3, jeu2_niv4, freq
    if debug: print "mjeu2"
    ouvert_jeu2 = 1
    jeu2_niv1 = 1
    jeu2_niv2 = 0
    jeu2_niv3 = 0
    jeu2_niv4 = 0
    jeu2 = Canvas(root, width=Largeur, height=Hauteur, bg='white')
    PosX2 = Largeur / 2
    PosY2 = Hauteur / 2
    PosX3 = Largeur / 2
    PosY3 = Hauteur / 2
    x0 = PosX2 - (Largeur / 15)
    y0 = PosY2 - (Largeur / 15)
    x1 = PosX2 + (Largeur / 15)
    y1 = PosY2 + (Largeur / 15)

    minmax = min(Largeur, Hauteur)

    counter_time = 0

    var2 = IntVar()

    # ~ compt_time()

    # Pion2 = disque qui change de taille
    # Pion3 = cercle intérieur
    # Pion4 = cercle extérieur
    # Pion5 = disque blanc pour cacher le disque gris
    # Pion6 = disque gris
    Pion6 = jeu2.create_oval((PosX2 - (Largeur / (3.3))), (PosY2 - (Largeur / (3.3))), (PosX2 + (Largeur / (3.3))),
                             (PosY2 + (Largeur / (3.3))), width=2, fill='light gray', outline='light gray',
                             dash=(10, 20))
    Pion5 = jeu2.create_oval((PosX2 - (Largeur / 5.2)), (PosY2 - (Largeur / 5.2)), (PosX2 + (Largeur / 5.2)),
                             (PosY2 + (Largeur / 5.2)), width=2, fill='white', outline='white')
    Pion2 = jeu2.create_oval(x0, y0, x1, y1, width=2, fill='lime green', outline='green4')
    Pion3 = jeu2.create_oval((PosX2 - (Largeur / 5.2)), (PosY2 - (Largeur / 5.2)), (PosX2 + (Largeur / 5.2)),
                             (PosY2 + (Largeur / 5.2)), width=2, outline='dark green', dash=(10, 20))
    Pion4 = jeu2.create_oval((PosX2 - (Largeur / (3.3))), (PosY2 - (Largeur / (3.3))), (PosX2 + (Largeur / (3.3))),
                             (PosY2 + (Largeur / (3.3))), width=2, outline='dark green', dash=(10, 20))

    # ~ Pion4 = jeu2.create_oval((PosX2-(Largeur/(4))), (PosY2-(Largeur/(4))),(PosX2+(Largeur/(4))),(PosY2+(Largeur/(4))),width=2, outline='spring green4', dash=(10,20))
    compt_time()
    Maintient = Label(jeu2, textvariable=var2, fg="black", bg="white", font="Verdana 55 bold")
    jeu2.focus_set()
    # Je le laisse car le jeu peux aussi se débuger au vlavier
    jeu2.bind('<Key>', Clavier2)

    # ~ quitter_jeu2 = Button(root, text='QUITTER LE JEU', command=quit_jeu2, fg="floral white", bg="spring green4", activeforeground="burlywood1", activebackground="spring green4", font="Verdana 14 bold")
    quitter_jeu2 = Button(root, text='QUITTER LE JEU', command=quit_jeu2, fg="floral white", bg="lime green",
                          activeforeground="floral white", activebackground="green yellow", font="Verdana 14 bold")
    quitter_jeu2.pack()
    quitter_jeu2.place(width=(Largeur / 7), height=(Hauteur / 19.5), relx=0.859, rely=0.951)

    Maintient.pack()
    Maintient.place(width=(Largeur / 10), height=(Hauteur / 13), relx=0.84, rely=0.2)

    if (debug):
        FreqAff = Label(jeu2, textvariable=freq, fg="black", bg="white", font="Verdana 30 bold")
        FreqAff.pack()
        FreqAff.place(relx=0.85, rely=0.1)

    jeu2.pack()
    button_detect()

    root.mainloop()


def update2():
    global debug, minmax, Pion2, PosX2, PosY2, Hauteur, Largeur, x0, y0, x1, y1, jeu2, jeu2_niv1, jeu2_niv2, jeu2_niv3, jeu2_niv4, freq

    if ouvert_jeu2 == 1:
        if debug: print"update2"

        # Valeur theremine:
        # Lecture frequence -> position
        # ~ if -minmax/2< Largeur/2-freq*minmax/MAX < minmax/2:
        if freq < MAX:
            x0 = Largeur / 2 - freq * minmax / MAX
            y0 = Hauteur / 2 - freq * minmax / MAX
            x1 = Largeur / 2 + freq * minmax / MAX
            y1 = Hauteur / 2 + freq * minmax / MAX

        if jeu2_niv1 == 1:
            if ((PosX2 - (Largeur / (3.3))) < x0 < PosX2 - (Largeur / 5.2) and (
                    PosY2 - (Largeur / (3.3))) < y0 < PosY2 - (Largeur / 5.2) and (
                    PosX2 + (Largeur / (3.3))) > x1 > PosX2 + (Largeur / 5.2) and (
                    PosY2 + (Largeur / (3.3))) > y1 > PosY2 + (Largeur / 5.2)):
                jeu2.itemconfig(Pion2, fill="green yellow", outline="SpringGreen4")

            else:
                jeu2.itemconfig(Pion2, fill="lime green", outline="SpringGreen4")

        if jeu2_niv2 == 1:
            if ((PosX2 - (Largeur / (3.6))) < x0 < PosX2 - (Largeur / 5) and (
                    PosY2 - (Largeur / (3.6))) < y0 < PosY2 - (Largeur / 5) and (
                    PosX2 + (Largeur / (3.6))) > x1 > PosX2 + (Largeur / 5) and (
                    PosY2 + (Largeur / (3.6))) > y1 > PosY2 + (Largeur / 5)):
                jeu2.itemconfig(Pion2, fill="gold", outline="dark orange")
            else:
                jeu2.itemconfig(Pion2, fill="goldenrod1", outline="dark orange")

        if jeu2_niv3 == 1:
            if ((PosX2 - (Largeur / (3.9))) < x0 < PosX2 - (Largeur / 4.8) and (
                    PosY2 - (Largeur / (3.9))) < y0 < PosY2 - (Largeur / 4.8) and (
                    PosX2 + (Largeur / (3.9))) > x1 > PosX2 + (Largeur / 4.8) and (
                    PosY2 + (Largeur / (3.9))) > y1 > PosY2 + (Largeur / 4.8)):
                jeu2.itemconfig(Pion2, fill="SteelBlue2", outline="DodgerBlue4")
            else:
                jeu2.itemconfig(Pion2, fill="DodgerBlue2", outline="DodgerBlue4")

        if jeu2_niv4 == 1:
            if ((PosX2 - (Largeur / (4.2))) < x0 < PosX2 - (Largeur / 4.8) and (
                    PosY2 - (Largeur / (4.2))) < y0 < PosY2 - (Largeur / 4.8) and (
                    PosX2 + (Largeur / (4.2))) > x1 > PosX2 + (Largeur / 4.8) and (
                    PosY2 + (Largeur / (4.2))) > y1 > PosY2 + (Largeur / 4.8)):
                jeu2.itemconfig(Pion2, fill="OrangeRed2", outline="red4")
            else:
                jeu2.itemconfig(Pion2, fill="red2", outline="red4")

        jeu2.coords(Pion2, x0, y0, x1, y1)

        # on limite les dimensions du disque pour pas qu'il soit trop grand ou trop petit
        if (x0 < PosX2 - (Largeur / 3) and y0 < PosY2 - (Largeur / 3) and x1 > PosX2 + (Largeur / 3) and y1 > PosY2 + (
                Largeur / 3)):
            jeu2.coords(Pion2, PosX2 - (Largeur / 3), PosY2 - (Largeur / 3), PosX2 + (Largeur / 3),
                        PosY2 + (Largeur / 3))

        if (x0 > PosX2 - (Largeur / 20) and y0 > PosY2 - (Largeur / 20) and x1 < PosX2 + (
                Largeur / 20) and y1 < PosY2 + (Largeur / 20)):
            jeu2.coords(Pion2, PosX2 - (Largeur / 20), PosY2 - (Largeur / 20), PosX2 + (Largeur / 20),
                        PosY2 + (Largeur / 20))


def compt_time():
    global debug, var2, counter_time, jeu2, PosX2, PosY2, Pion2, Hauteur, Largeur, Maintient, jeu2_niv1, jeu2_niv2, jeu2_niv3, jeu2_niv4, ouvert_jeu2
    if debug: print "compt_time"
    if ouvert_jeu2 == 1:
        if jeu2_niv1 == 1:
            if ((PosX2 - (Largeur / (3.3))) < x0 < PosX2 - (Largeur / 5.2) and (
                    PosY2 - (Largeur / (3.3))) < y0 < PosY2 - (Largeur / 5.2) and (
                    PosX2 + (Largeur / (3.3))) > x1 > PosX2 + (Largeur / 5.2) and (
                    PosY2 + (Largeur / (3.3))) > y1 > PosY2 + (Largeur / 5.2)):
                counter_time = counter_time + 1
                if counter_time >= 30:
                    Maintient.configure(fg='red')
                    if counter_time >= 31:
                        time.sleep(1)
                        passer_jeu2_niv2()
                if counter_time < 30:
                    Maintient.configure(fg='black')
            else:
                counter_time = 0

        if jeu2_niv2 == 1:
            if ((PosX2 - (Largeur / (3.6))) < x0 < PosX2 - (Largeur / 5) and (
                    PosY2 - (Largeur / (3.6))) < y0 < PosY2 - (Largeur / 5) and (
                    PosX2 + (Largeur / (3.6))) > x1 > PosX2 + (Largeur / 5) and (
                    PosY2 + (Largeur / (3.6))) > y1 > PosY2 + (Largeur / 5)):
                counter_time = counter_time + 1
                if counter_time >= 30:
                    Maintient.configure(fg='red')
                    if counter_time >= 31:
                        time.sleep(1)
                        passer_jeu2_niv3()
                if counter_time < 30:
                    Maintient.configure(fg='black')
            else:
                counter_time = 0

        if jeu2_niv3 == 1:
            if ((PosX2 - (Largeur / (3.9))) < x0 < PosX2 - (Largeur / 4.8) and (
                    PosY2 - (Largeur / (3.9))) < y0 < PosY2 - (Largeur / 4.8) and (
                    PosX2 + (Largeur / (3.9))) > x1 > PosX2 + (Largeur / 4.8) and (
                    PosY2 + (Largeur / (3.9))) > y1 > PosY2 + (Largeur / 4.8)):
                counter_time = counter_time + 1
                if counter_time >= 30:
                    Maintient.configure(fg='red')
                    if counter_time >= 31:
                        time.sleep(1)
                        passer_jeu2_niv4()
                if counter_time < 30:
                    Maintient.configure(fg='black')
            else:
                counter_time = 0

        if jeu2_niv4 == 1:
            if ((PosX2 - (Largeur / (4.2))) < x0 < PosX2 - (Largeur / 4.8) and (
                    PosY2 - (Largeur / (4.2))) < y0 < PosY2 - (Largeur / 4.8) and (
                    PosX2 + (Largeur / (4.2))) > x1 > PosX2 + (Largeur / 4.8) and (
                    PosY2 + (Largeur / (4.2))) > y1 > PosY2 + (Largeur / 4.8)):
                counter_time = counter_time + 1
                if counter_time >= 30:
                    Maintient.configure(fg='red')
                    if counter_time >= 31:
                        time.sleep(1)
                        fin_jeu2()
                if counter_time < 30:
                    Maintient.configure(fg='black')
            else:
                counter_time = 0

        update2()
        root.after(90, compt_time)

        var2.set(counter_time)


def passer_jeu2_niv2():
    global debug, Pion2, Pion3, Pion4, Pion5, Pion6, PosX2, PosY2, Hauteur, Largeur, x0, y0, x1, y1, jeu2, counter_time, jeu2_niv1, jeu2_niv2, jeu2_niv3, jeu2_niv4, quitter_jeu2
    if debug: print "passer_jeu2_niv2"
    counter_time = 0
    jeu2_niv1 = 0
    jeu2_niv2 = 1
    jeu2_niv3 = 0
    jeu2_niv4 = 0
    Maintient.configure(fg='black')
    jeu2.itemconfig(Pion2, fill="goldenrod1", outline="dark orange")
    jeu2.itemconfig(Pion3, outline="DarkOrange1")
    jeu2.itemconfig(Pion4, outline="DarkOrange1")
    quitter_jeu2.configure(bg='goldenrod1', fg='floral white', activebackground='gold', activeforeground='floral white')
    x0 = PosX2 - (Largeur / 15)
    y0 = PosY2 - (Largeur / 15)
    x1 = PosX2 + (Largeur / 15)
    y1 = PosY2 + (Largeur / 15)
    jeu2.coords(Pion2, x0, y0, x1, y1)
    jeu2.coords(Pion3, (PosX2 - (Largeur / (5))), (PosY2 - (Largeur / (5))), (PosX2 + (Largeur / (5))),
                (PosY2 + (Largeur / (5))))
    jeu2.coords(Pion4, (PosX2 - (Largeur / (3.6))), (PosY2 - (Largeur / (3.6))), (PosX2 + (Largeur / (3.6))),
                (PosY2 + (Largeur / (3.6))))
    jeu2.coords(Pion5, (PosX2 - (Largeur / (5))), (PosY2 - (Largeur / (5))), (PosX2 + (Largeur / (5))),
                (PosY2 + (Largeur / (5))))
    jeu2.coords(Pion6, (PosX2 - (Largeur / (3.6))), (PosY2 - (Largeur / (3.6))), (PosX2 + (Largeur / (3.6))),
                (PosY2 + (Largeur / (3.6))))


def passer_jeu2_niv3():
    global debug, Pion2, Pion3, Pion4, PosX2, PosY2, Hauteur, Largeur, x0, y0, x1, y1, jeu2, counter_time, jeu2_niv1, jeu2_niv2, jeu2_niv3, jeu2_niv4, quitter_jeu2
    if debug: print "passer_jeu2_niv3"
    counter_time = 0
    jeu2_niv1 = 0
    jeu2_niv2 = 0
    jeu2_niv3 = 1
    jeu2_niv4 = 0
    Maintient.configure(fg='black')
    jeu2.itemconfig(Pion2, fill="red2", outline="red3")
    jeu2.itemconfigure(Pion3, outline="blue2")
    jeu2.itemconfigure(Pion4, outline="blue2")
    quitter_jeu2.configure(bg='DodgerBlue2', fg='floral white', activebackground='SteelBlue2',
                           activeforeground='floral white')
    x0 = PosX2 - (Largeur / 15)
    y0 = PosY2 - (Largeur / 15)
    x1 = PosX2 + (Largeur / 15)
    y1 = PosY2 + (Largeur / 15)
    jeu2.coords(Pion2, x0, y0, x1, y1)
    # jeu2.coords(Pion3,(PosX2-(Largeur/(4.8))), (PosY2-(Largeur/(4.8))),(PosX2+(Largeur/(4.8))),(PosY2+(Largeur/(4.8))))
    # jeu2.coords(Pion4, (PosX2-(Largeur/(4.5))), (PosY2-(Largeur/(4.5))),(PosX2+(Largeur/(4.5))),(PosY2+(Largeur/(4.5))))
    jeu2.coords(Pion3, (PosX2 - (Largeur / (4.8))), (PosY2 - (Largeur / (4.8))), (PosX2 + (Largeur / (4.8))),
                (PosY2 + (Largeur / (4.8))))
    jeu2.coords(Pion4, (PosX2 - (Largeur / (3.9))), (PosY2 - (Largeur / (3.9))), (PosX2 + (Largeur / (3.9))),
                (PosY2 + (Largeur / (3.9))))
    jeu2.coords(Pion5, (PosX2 - (Largeur / (4.8))), (PosY2 - (Largeur / (4.8))), (PosX2 + (Largeur / (4.8))),
                (PosY2 + (Largeur / (4.8))))
    jeu2.coords(Pion6, (PosX2 - (Largeur / (3.9))), (PosY2 - (Largeur / (3.9))), (PosX2 + (Largeur / (3.9))),
                (PosY2 + (Largeur / (3.9))))


def passer_jeu2_niv4():
    global debug, Pion2, Pion3, Pion4, PosX2, PosY2, Hauteur, Largeur, x0, y0, x1, y1, jeu2, counter_time, jeu2_niv1, jeu2_niv2, jeu2_niv3, jeu2_niv4, quitter_jeu2
    if debug: print "passer_jeu2_niv4"
    counter_time = 0
    jeu2_niv1 = 0
    jeu2_niv2 = 0
    jeu2_niv3 = 0
    jeu2_niv4 = 1
    Maintient.configure(fg='black')
    jeu2.itemconfig(Pion2, fill="red2", outline="red4")
    jeu2.itemconfigure(Pion3, outline="brown4")
    jeu2.itemconfigure(Pion4, outline="brown4")
    quitter_jeu2.configure(bg='red2', fg='floral white', activebackground='OrangeRed2', activeforeground='floral white')
    x0 = PosX2 - (Largeur / 15)
    y0 = PosY2 - (Largeur / 15)
    x1 = PosX2 + (Largeur / 15)
    y1 = PosY2 + (Largeur / 15)
    jeu2.coords(Pion2, x0, y0, x1, y1)
    jeu2.coords(Pion3, (PosX2 - (Largeur / (4.8))), (PosY2 - (Largeur / (4.8))), (PosX2 + (Largeur / (4.8))),
                (PosY2 + (Largeur / (4.8))))
    jeu2.coords(Pion4, (PosX2 - (Largeur / (4.2))), (PosY2 - (Largeur / (4.2))), (PosX2 + (Largeur / (4.2))),
                (PosY2 + (Largeur / (4.2))))
    jeu2.coords(Pion5, (PosX2 - (Largeur / (4.8))), (PosY2 - (Largeur / (4.8))), (PosX2 + (Largeur / (4.8))),
                (PosY2 + (Largeur / (4.8))))
    jeu2.coords(Pion6, (PosX2 - (Largeur / (4.2))), (PosY2 - (Largeur / (4.2))), (PosX2 + (Largeur / (4.2))),
                (PosY2 + (Largeur / (4.2))))


def quit_jeu2():
    global jeu2, quitter_jeu2, ouvert_jeu2
    if debug: print "quit_jeu2"
    ouvert_jeu2 = 0
    quitter_jeu2.destroy()
    jeu2.destroy()
    lancer_menu()


def fin_jeu2():
    global debug, jeu2, quitter_jeu2, ouvert_jeu2
    if debug: print "fin_jeu2"
    ouvert_jeu2 = 0
    quitter_jeu2.destroy()
    jeu2.destroy()
    winning2()


def winning2():
    global debug, win2, recommencer2, quit_winning2, ouvert_win2, list_win2, choix_win2
    if debug: print "winning2"
    ouvert_win2 = 1
    list_win2 = [1, 0]
    choix_win2 = 0
    win2 = Canvas(root, width=Largeur, height=Hauteur, bg='white')
    win2.focus_set()
    # win2.bind('<Key>',gerer_choix3)

    gagne = Label(win2, text="Bravo !", fg="deep pink", bg="white", font="Verdana 70 bold")
    gagne.pack()
    gagne.place(width=(Largeur / 3), height=(Hauteur / 11), relx=0.34, rely=0.17)
    gagne2 = Label(win2, text="Que faire ?", fg="hot pink", bg="white", font="Verdana 30 bold")
    gagne2.pack()
    gagne2.place(width=(Largeur / 3), height=(Hauteur / 12), relx=0.34, rely=0.35)

    recommencer2 = Button(root, text='RECOMMENCER', command=recommencer_jeu2, font="Verdana 20 bold", fg="white",
                          bg="green", activebackground="hot pink", activeforeground="white", width=Largeur / 60)
    recommencer2.pack()
    recommencer2.place(width=(Largeur / 3), height=(Largeur / 21), relx=0.34, rely=0.6)
    quit_winning2 = Button(root, text='QUITTER', command=quit_win2, fg="white", bg="deep pink",
                           activebackground="hot pink", activeforeground="white", font="Verdana 20 bold",
                           width=Largeur / 60)
    quit_winning2.pack()
    quit_winning2.place(width=(Largeur / 3), height=(Largeur / 21), relx=0.34, rely=0.7)
    win2.pack(padx=0, pady=0)

    button_detect()
    root.mainloop()


def quit_win2():
    global debug, win2, recommencer2, quit_winning2, ouvert_win2
    if debug: print "quit_win2"
    ouvert_win2 = 0
    recommencer2.destroy()
    quit_winning2.destroy()
    win2.destroy()
    lancer_menu()


def recommencer_jeu2():
    global debug, win2, recommencer2, quit_winning2, ouvert_win2
    if debug: print "recommencer_jeu2"
    ouvert_win2 = 0
    recommencer2.destroy()
    quit_winning2.destroy()
    win2.destroy()
    mjeu2()


# ----------------------------------------------------------------------
#                               JEU 3
# ----------------------------------------------------------------------
def mjeu3():
    global jeu3, disc1, disc2, cpt_jeu3, var3, disc1_col, disc2_col, lock_jeu3, possible1_jeu3, possible2_jeu3, disc1_realcolor, quitter_jeu3, ouvert_jeu3, quitter_jeu3
    global jeu3_chgt1, jeu3_chgt2, jeu3_chgt3, jeu3_chgt4, cpt_jeu3_chgt
    ouvert_jeu3 = 1
    jeu3 = Canvas(root, width=Largeur, height=Hauteur, bg="white")
    Pos_d1X = Largeur / 4
    Pos_d1Y = Hauteur / 2
    Pos_d2X = Largeur - Largeur / 4
    Pos_d2Y = Hauteur / 2

    Pos_jeu3_chgt1X = Largeur / 2.6
    Pos_jeu3_chgt1Y = Hauteur - Hauteur / 8

    Pos_jeu3_chgt2X = Largeur / 2.2
    Pos_jeu3_chgt2Y = Hauteur - Hauteur / 8

    Pos_jeu3_chgt3X = Largeur / 1.9
    Pos_jeu3_chgt3Y = Hauteur - Hauteur / 8

    Pos_jeu3_chgt4X = Largeur / 1.67
    Pos_jeu3_chgt4Y = Hauteur - Hauteur / 8

    cpt_jeu3 = 0
    disc1_col = 0
    disc2_col = 0
    disc1_realcolor = 0
    lock_jeu3 = 0
    possible1_jeu3 = 0
    possible2_jeu3 = 0

    cpt_jeu3_chgt = 0

    var3 = IntVar()

    comptage_jeu3()

    disc1 = jeu3.create_oval((Pos_d1X - (Largeur / 6)), (Pos_d1Y - (Largeur / 6)), (Pos_d1X + (Largeur / 6)),
                             (Pos_d1Y + (Largeur / 6)), width=2, fill="blue", outline="blue")
    disc2 = jeu3.create_oval((Pos_d2X - (Largeur / 6)), (Pos_d2Y - (Largeur / 6)), (Pos_d2X + (Largeur / 6)),
                             (Pos_d2Y + (Largeur / 6)), width=2, fill="blue", outline="blue")

    jeu3_chgt1 = jeu3.create_oval((Pos_jeu3_chgt1X - (Largeur / 50)), (Pos_jeu3_chgt1Y - (Largeur / 50)),
                                  (Pos_jeu3_chgt1X + (Largeur / 50)), (Pos_jeu3_chgt1Y + (Largeur / 50)), width=2,
                                  fill="white", outline="blue")
    jeu3_chgt2 = jeu3.create_oval((Pos_jeu3_chgt2X - (Largeur / 50)), (Pos_jeu3_chgt2Y - (Largeur / 50)),
                                  (Pos_jeu3_chgt2X + (Largeur / 50)), (Pos_jeu3_chgt2Y + (Largeur / 50)), width=2,
                                  fill="white", outline="blue")
    jeu3_chgt3 = jeu3.create_oval((Pos_jeu3_chgt3X - (Largeur / 50)), (Pos_jeu3_chgt3Y - (Largeur / 50)),
                                  (Pos_jeu3_chgt3X + (Largeur / 50)), (Pos_jeu3_chgt3Y + (Largeur / 50)), width=2,
                                  fill="white", outline="blue")
    jeu3_chgt4 = jeu3.create_oval((Pos_jeu3_chgt4X - (Largeur / 50)), (Pos_jeu3_chgt4Y - (Largeur / 50)),
                                  (Pos_jeu3_chgt4X + (Largeur / 50)), (Pos_jeu3_chgt4Y + (Largeur / 50)), width=2,
                                  fill="white", outline="red")

    compt_jeu3 = Label(jeu3, textvariable=var3, fg="black", bg="white", font="Verdana 22 bold")

    compt_jeu3.pack()
    compt_jeu3.place(relx=0.85, rely=0.2)

    quitter_jeu3 = Button(root, text='QUITTER LE JEU', command=quit_jeu3, fg="floral white", bg="cyan",
                          activeforeground="floral white", activebackground="green yellow", font="Verdana 14 bold")
    quitter_jeu3.pack()
    quitter_jeu3.place(width=(Largeur / 7), height=(Hauteur / 19.5), relx=0.859, rely=0.951)

    anime3_possible1_debut()

    update3()

    jeu3.focus_set()
    jeu3.bind('<Key>', Clavier3)

    jeu3.pack()

    button_detect()

    root.mainloop()


def anime3_possible1_debut():
    global jeu3, disc1, disc1_col, possible1_jeu3, possible2_jeu3

    if ouvert_jeu3 == 1:
        disc1_col = 1
        possible1_jeu3 = 1

        root.after(500, anime3_possible1)


def anime3_possible1():
    global jeu3, disc1, disc1_col, possible1_jeu3, possible2_jeu3, disc1_realcolor

    if ouvert_jeu3 == 1:
        jeu3.itemconfig(disc1, fill="red", outline="red")
        disc1_realcolor = 1

        root.after(500, anime3_possible1_fin)


def anime3_possible1_fin():
    global jeu3, disc1, disc1_col, possible1_jeu3, possible2_jeu3

    if ouvert_jeu3 == 1:
        possible1_jeu3 = 0

        root.after(1000, anime3_possible2_debut)


def anime3_possible2_debut():
    global jeu3, disc1, disc1_col, possible1_jeu3, possible2_jeu3

    if ouvert_jeu3 == 1:
        disc1_col = 0
        possible2_jeu3 = 1

        root.after(500, anime3_possible2)


def anime3_possible2():
    global jeu3, disc1, disc1_col, possible1_jeu3, possible2_jeu3, disc1_realcolor

    if ouvert_jeu3 == 1:
        jeu3.itemconfig(disc1, fill="blue", outline="blue")
        jeu3_lancement_chgt()
        disc1_realcolor = 0

        root.after(500, anime3_possible2_fin)


def anime3_possible2_fin():
    global jeu3, disc1, disc1_col, possible1_jeu3, possible2_jeu3

    if ouvert_jeu3 == 1:
        possible2_jeu3 = 0

        root.after(1000, anime3_possible1_debut)


def comptage_jeu3():
    global cpt_jeu3, var3, disc1_col, disc2_col, lock_jeu3, possible1_jeu3, possible2_jeu3, disc1_realcolor

    if ouvert_jeu3 == 1:

        if (cpt_jeu3 >= 3):
            time.sleep(1)
            fin_jeu3()

        if possible1_jeu3 == 1:
            if lock_jeu3 == 0:
                if (disc1_col == 1 and disc2_col == 1):
                    cpt_jeu3 = cpt_jeu3 + 1

                    lock_jeu3 = 1

        if possible1_jeu3 == 0:
            lock_jeu3 = 0

        if (possible2_jeu3 == 0 and possible1_jeu3 == 0):
            if ((disc1_realcolor == 1 and disc2_col == 0) or (disc1_realcolor == 0 and disc2_col == 1)):
                cpt_jeu3 = 0

        var3.set(cpt_jeu3)

        root.after(100, comptage_jeu3)


def jeu3_lancement_chgt():
    global jeu3, jeu3_chgt1, jeu3_chgt2, jeu3_chgt3, jeu3_chgt4, disc1_realcolor, cpt_jeu3_chgt
    if ouvert_jeu3 == 1:
        jeu3.itemconfig(jeu3_chgt1, fill="white", outline="blue")
        jeu3.itemconfig(jeu3_chgt2, fill="white", outline="blue")
        jeu3.itemconfig(jeu3_chgt3, fill="white", outline="blue")
        jeu3.itemconfig(jeu3_chgt4, fill="white", outline="red")

        if cpt_jeu3_chgt < 3:
            cpt_jeu3_chgt = cpt_jeu3_chgt + 1
            root.after(500, jeu3_act_chgt1)

        if cpt_jeu3_chgt == 3:
            jeu3.itemconfig(jeu3_chgt1, fill="white", outline="white")
            jeu3.itemconfig(jeu3_chgt2, fill="white", outline="white")
            jeu3.itemconfig(jeu3_chgt3, fill="white", outline="white")
            jeu3.itemconfig(jeu3_chgt4, fill="white", outline="white")


def jeu3_act_chgt1():
    global jeu3, jeu3_chgt1, disc1_realcolor
    if ouvert_jeu3 == 1:
        jeu3.itemconfig(jeu3_chgt1, fill="blue", outline="blue")
        root.after(500, jeu3_act_chgt2)


def jeu3_act_chgt2():
    global jeu3, jeu3_chgt2, disc1_realcolor
    if ouvert_jeu3 == 1:
        jeu3.itemconfig(jeu3_chgt2, fill="blue", outline="blue")
        root.after(500, jeu3_act_chgt3)


def jeu3_act_chgt3():
    global jeu3, jeu3_chgt3, disc1_realcolor
    if ouvert_jeu3 == 1:
        jeu3.itemconfig(jeu3_chgt3, fill="blue", outline="blue")
        root.after(500, jeu3_act_chgt4)


def jeu3_act_chgt4():
    global jeu3, jeu3_chgt4, disc1_realcolor
    if ouvert_jeu3 == 1:
        jeu3.itemconfig(jeu3_chgt4, fill="red", outline="red")


def update3():
    global jeu3, disc1, disc2, disc1_col, disc2_col, freq

    if ouvert_jeu3 == 1:

        if freq <= (MAX / 2):
            disc2_col = 1
            jeu3.itemconfig(disc2, fill="red", outline="red")

        if freq > (MAX / 2):
            disc2_col = 0
            jeu3.itemconfig(disc2, fill="blue", outline="blue")

        root.after(100, update3)


def quit_jeu3():
    global jeu3, quitter_jeu3, ouvert_jeu3
    if debug: print "quit_jeu3"
    ouvert_jeu3 = 0
    quitter_jeu3.destroy()
    jeu3.destroy()
    lancer_menu()


def fin_jeu3():
    global debug, jeu3, quitter_jeu3, ouvert_jeu3
    if debug: print "fin_jeu3"
    ouvert_jeu3 = 0
    quitter_jeu3.destroy()
    jeu3.destroy()
    winning3()


def winning3():
    global debug, win3, recommencer3, quit_winning3, ouvert_win3, list_win3, choix_win3
    if debug: print "winning3"
    ouvert_win3 = 1
    list_win3 = [1, 0]
    choix_win3 = 0
    win3 = Canvas(root, width=Largeur, height=Hauteur, bg='white')
    win3.focus_set()

    gagne_jeu3 = Label(win3, text="Bravo !", fg="deep pink", bg="white", font="Verdana 70 bold")
    gagne_jeu3.pack()
    gagne_jeu3.place(width=(Largeur / 3), height=(Hauteur / 11), relx=0.34, rely=0.17)
    gagne2_jeu3 = Label(win3, text="Que faire ?", fg="hot pink", bg="white", font="Verdana 30 bold")
    gagne2_jeu3.pack()
    gagne2_jeu3.place(width=(Largeur / 3), height=(Hauteur / 12), relx=0.34, rely=0.35)

    recommencer3 = Button(root, text='RECOMMENCER', command=recommencer_jeu3, font="Verdana 20 bold", fg="white",
                          bg="green", activebackground="hot pink", activeforeground="white", width=Largeur / 60)
    recommencer3.pack()
    recommencer3.place(width=(Largeur / 3), height=(Largeur / 21), relx=0.34, rely=0.6)
    quit_winning3 = Button(root, text='QUITTER', command=quit_win3, fg="white", bg="deep pink",
                           activebackground="hot pink", activeforeground="white", font="Verdana 20 bold",
                           width=Largeur / 60)
    quit_winning3.pack()
    quit_winning3.place(width=(Largeur / 3), height=(Largeur / 21), relx=0.34, rely=0.7)
    win3.pack(padx=0, pady=0)

    button_detect()
    root.mainloop()


def quit_win3():
    global debug, win3, recommencer3, quit_winning3, ouvert_win3
    if debug: print "quit_win3"
    ouvert_win3 = 0
    recommencer3.destroy()
    quit_winning3.destroy()
    win3.destroy()
    lancer_menu()


def recommencer_jeu3():
    global debug, win3, recommencer3, quit_winning3, ouvert_win3
    if debug: print "recommencer_jeu3"
    ouvert_win3 = 0
    recommencer3.destroy()
    quit_winning3.destroy()
    win3.destroy()
    mjeu3()


# ======================================================================
#                               MAIN
# ======================================================================
path = os.path.dirname(__file__)  # Chemin absolu du script python
root = Tk()  # Creation du moteur graphique
root.title('REST')

#               --------------------------------
# J'ai commenté les lignes suivantes pour tester en console
#
#               --------------------------------
root.overrideredirect(0)
# Largeur = 800
# Hauteur = 500

Largeur = root.winfo_screenwidth()
Hauteur = root.winfo_screenheight()

root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (Largeur, Hauteur))
root.attributes("-fullscreen", 1)

ferme_quit = 0
ouvert_menu = 0
ouvert_trans1 = 0
ouvert_trans2 = 0
ouvert_trans3 = 0
ouvert_cal = 0
select_jeu1 = 0
select_jeu2 = 0
ouvert_jeu1 = 0
ouvert_jeu2 = 0
ouvert_jeu3 = 0
ouvert_lose1 = 0
ouvert_win2 = 0
ouvert_win3 = 0

# On appelle la lecture des ports usb et elle se lancera toujours automatiquement
read()
# Menu
lancer_menu()

root.mainloop()

usb_port.close()
GPIO.cleanup()

import time
from tkinter import *
import random
import copy


def detecte_vivant_bord(tab):
    """
    Parcourt la bordure du tableau et retourne True
    s'il y a au moins un 1 (une cellule vivante)
    """
    # on parcourt la première ligne :
    for elem in tab[0]:
        if elem == 1:
            return True
    # on parcourt la dernière ligne :
    for elem in tab[-1]:
        if elem == 1:
            return True
    # on parcourt la première et la dernière colonne :
    for line in tab:
        if line[0] == 1 or line[-1] == 1:
            return True
    # et sinon
    return False


def ajoute_couronne(tab):
    """
    Retourne un nouveau tableau construit sur tab sur
    lequel on a ajouté une couronne de 0
    """
    nb_line = len(tab)
    nb_col = len(tab[0])
    T = [[0 for col in range(nb_col+2)] for line in range(nb_line+2)]
    for i in range(nb_line):
        for j in range(nb_col):
            T[i+1][j+1] = tab[i][j]
    return T


def enleve_couronne(tab):
    """
    Retourne un nouveau tableau construit sur tab sur
    lequel on a enlevé la couronne (de 0) extérieure
    """
    nb_line = len(tab)
    nb_col = len(tab[0])
    T = [[0 for col in range(nb_col-2)] for line in range(nb_line-2)]
    for i in range(1, nb_line-1):
        for j in range(1, nb_col-1):
            T[i-1][j-1] = tab[i][j]
    return T


def nb_vivantes(tab, case):
    """
    Retourne le nombre de cellules vivantes autour de la case
    """
    line, col = case
    som = 0
    for i in range(line-1, line+2):
        for j in range(col-1, col+2):
            try: som = som + tab[i][j]
            except: print(case)
    if tab[line][col] == 1:
        return som-1
    else:
        return som


def modifier_case(tab, case, Tab):
    """
    Modifie la valeur de la case en fonction des règles.
    On utilise un tableau tampon pour ne pas fausser les calculs suivants.
    """
    vivantes = nb_vivantes(tab, case)
    line, col = case
    if tab[line][col] == 1:     # si la cellule est vivante
        if 2 <= vivantes <= 3:  # et qu'elle est entourée de 2 ou 3 vivantes
            Tab[line][col] = 1  # alors elle reste vivante
        else:                   # sinon
            Tab[line][col] = 0  # elle meurt
    if tab[line][col] == 0:     # si la cellule est morte
        if vivantes == 3:       # mais qu'elle est entourée de 3 vivantes
            Tab[line][col] = 1  # alors elle naît
        else:                   # sinon
            Tab[line][col] = 0  # elle reste morte


def quadrillage(zone, tab):
    lines = len(tab)
    cols = len(tab[0])
    W = int(zone["width"])
    w = W / cols
    h = H / lines
    for i in range(lines):
        zone.create_line(i*w, 0, i*w, H)
        zone.create_line(0, i*h, W, i*h)


def tab_vers_graph(case, tab):
    line, col = case
    lines = len(tab)
    cols = len(tab[0])
    w = W / cols
    h = H / lines
    x = col * w + w / 2
    y = line * h + h / 2
    return x, y


def affichage(zone, tab):
    zone.delete('all')
    quadrillage(zone, tab)
    lines = len(tab)
    cols = len(tab[0])
    W = int(zone["width"])
    w = W / cols
    h = H / lines
    for line in range(lines):
        for col in range(cols):
            if tab[line][col]:
                x, y = tab_vers_graph((line, col), tab)
                zone.create_rectangle(x-w/2, y-h/2,x+h/2, y+h/2, fill="black")


def next_generation(tab):
    if detecte_vivant_bord(tab):
        tab = ajoute_couronne(tab)
    trav = copy.deepcopy(tab)
    trav = ajoute_couronne(trav)
    tampon = [[0 for i in range(len(trav))] for j in range(len(trav[0]))]
    for i in range(1, len(tab)):
        for j in range(1, len(tab)-1):
            modifier_case(trav, (i, j), tampon)
    tampon = enleve_couronne(tampon)
    return tampon


def jeu():
    global TAB, can
    TAB = next_generation(TAB)
    affichage(can, TAB)
    fen.after(1000, jeu)

################################################################################
#                   Fonction principale                                        #
################################################################################

## 1) s'il y a un 1 sur les bords, on ajoute tout de suite une couronne de 0
## 2) on construit un tableau de "travail" ayant une couronne de 0 en plus par
##    rapport au tableau réel (pour traiter toutes les cases de la même manière)
## 3) on parcourt ce tableau de "travail" (sans la couronne) et on modifie les
##    les cases d'un tableau tampon (même dimension que le travail) en fonction
##    des règles
## 4) on remplace le tableau réel par le tableau tampon (attention il faut
##    retirer la couronne.


fen = Tk()
fen.title("Jeu de la vie")

W, H = 500, 500

can = Canvas(fen, width=W, height=H)
can.pack()

TAB = [[random.randint(0, 1) for i in range(10)] for j in range(10)]
affichage(can, TAB)

jeu()

fen.mainloop()

#Map_fonction.py
import sys
import tkinter as tk
from Fonction.map import *

###############################################################################
# Section 1: Gestion des Maps
###############################################################################

def map_disponible():
    """
    Retourne une liste des cartes disponibles avec leurs titres et identifiants.

    Returns:
        list: Liste de tuples (identifiant, titre)
    """
    maps = all_maps()
    return [(key, maps[key]['title']) for key in maps]

def affichage_map():
    """
    Affiche la liste des maps disponibles avec leurs titres.

    Returns:
        maps (list): Liste des tuples (identifiant, titre)
    """
    maps = map_disponible()
    print(f"Maps disponibles : {len(maps)}")
    for i, (map_id, title) in enumerate(maps, 1):
        print(f"{i}. {title} ({map_id})")
    return maps

def select_map(maps):
    """
    Permet à l'utilisateur de sélectionner une map avec gestion des erreurs.

    Args:
        maps (list): Liste des tuples (identifiant, titre)

    Returns:
        tuple: (choix,map_choix, tours, tour_spawn_fantome) - Matrice de la map et variables de jeu
    """
    while True:
        try:
            choix = int(input("Choisir le numéro de la map (1, 2 ou 3) | '0' pour quitter: "))
            if choix == 0:
                sys.exit("Arrêt du programme demandé")
            elif 1 <= choix <= len(maps):
                map_id, _ = maps[choix - 1]
                selected_map = all_maps()[map_id]
                map_function = selected_map['function']
                map_choix, tours, tour_spawn_fantome = map_function()
                print(f"Vous avez choisi : {selected_map['title']}")
                return choix,map_choix, tours, tour_spawn_fantome
        except ValueError:
            print("Oops! mauvais type...")
        print(f"Veuillez choisir un nombre entre 1 et {len(maps)}")


def taille_map(map_choix):
    """
    Calcule la taille optimale des tuiles en fonction de la résolution d'écran.

    Args:
        map_choix (list): Matrice de la map sélectionnée

    Returns:
        taille (int): Taille optimale d'une tuile en pixels
    """
    # Configuration initiale de la fenêtre Tkinter
    root = tk.Tk()
    screen_width = int(root.winfo_screenwidth() * 0.6)
    screen_height = int(root.winfo_screenheight() * 0.9)
    root.destroy()

    # Calcul des dimensions
    map_width = len(map_choix[0])
    map_height = len(map_choix)

    # Calcul de la taille optimale
    taille_width = screen_width // map_width
    taille_height = screen_height // map_height
    return min(taille_width, taille_height)


def creation_map(g,a,b, map_choix, taille, map_objet):
    """
    Crée la représentation graphique de la map avec tous ses éléments.

    Args:
        g: Instance de la fenêtre graphique
        a (int): Largeur de la zone de jeu
        b (int): Longueur de la zone de jeu
        map_choix (list): Matrice de la map
        taille (int): Taille d'une tuile
        map_objet (list): Liste pour stocker les objets de la map

    Returns:
        tuple: (perso, ethernet) - Références aux objets du joueur et de la prise ethernet
    """
    perso = None
    ethernet = None

    # Création des couleur de fond terrain de jeu
    g.dessinerRectangle(0, 0, a, b + taille, "green")

    # Création de la grille
    for y_ligne in range(0, a, taille):
        g.dessinerLigne(y_ligne, 0, y_ligne, b + taille, "black")
    for x_ligne in range(0, b, taille):
        g.dessinerLigne(0, x_ligne, a, x_ligne, "black")

    for y in range(len(map_choix)):
        for x in range(len(map_choix[y])):
            case = map_choix[y][x]
            if case == "C":
                g.afficherImage(x * taille, y * taille, "Image/Images_resize/Colonne_resize.png")
            elif case == "M":
                mur = g.afficherImage(x * taille, y * taille, "Image/Images_resize/Mur_resize.png")
                map_objet.append(mur)
            elif case == "P":
                perso = g.afficherImage(x * taille, y * taille, "Image/Images_resize/Perso_droite_resize.png")
                map_objet.append(perso)
            elif case == "E":
                ethernet = g.afficherImage(x * taille, y * taille, "Image/Images_resize/Ethernet_resize.png")
                map_objet.append(ethernet)
    return perso, ethernet


def matrice(map_choix):
    """
    Affiche la matrice de la map dans la console pour le débogage.

    Args:
        map_choix (list): Matrice de la map à afficher
    """
    print("Matrice :")
    for ligne in map_choix:
        print(''.join(ligne))
    print()

def barre_score(g, taille, a, b, score, vies, lv, tour, portee_bombe):
    """
    Crée et affiche la barre de score avec toutes les informations du jeu.

    Args:
        g: Instance de la fenêtre graphique
        taille (int): Taille d'une tuile
        a (int): Largeur de la zone de jeu
        b (int): Longueur de la zone de jeu
        score (int): Score actuel
        vies (int): Nombre de vies restantes
        lv (int): Niveau actuel
        tour (int): nombre de tour restant
        portee_bombe (int): la porté d'une bombe
    Returns:
        tuple: (texte_vies, texte_score, texte_tour, texte_lv, texte_portee_bombe) - Référence mise à jour du texte des vies et le nouveau nombre de vies.
    """

    # Création des zones de fond
    g.dessinerRectangle(a, 0, a * 1.5, b + taille, "white")

    # Lignes de séparation barre des scores
    g.dessinerLigne(a + a // 7, taille * 1, a + a * 0.35, taille * 1, "black")
    g.dessinerLigne(a + a // 7, taille * 2, a + a * 0.35, taille * 2, "black")
    g.dessinerLigne(a + a // 7, taille * 3, a + a * 0.35, taille * 3, "black")
    g.dessinerLigne(a + a // 7, taille * 4, a + a * 0.35, taille * 4, "black")

    # Affichage des info du joueurs dans l'ordre d'affichage
    texte_tour = g.afficherTexte(f"Left turn: {tour}", a + a // 4, taille // 2, "green", taille // 4)
    texte_score = g.afficherTexte(f"Score: {score}", a + a // 4, taille * 1.5, "black", taille // 4)
    texte_vies = g.afficherTexte(f"Vies: {vies}", a + a // 4, taille * 2.5, "green", taille // 4)
    texte_lv = g.afficherTexte(f"Lv: {lv}", a + a // 4, taille * 3.5, "black", taille // 4)
    texte_portee_bombe = g.afficherTexte(f"Portée bombe: {portee_bombe}", a + a // 4, taille * 4.5, "black",
                                         taille // 4)
    return texte_vies, texte_score, texte_tour, texte_lv, texte_portee_bombe


# Gestion de la vie du joueur (texte_vie)
def degats_compteur(g, a, taille,vies, texte_vies):
    """
    Met à jour l'affichage des vies d'un joueur après avoir subi des dégâts.

    Args:
        g: Instance de la fenêtre graphique utilisée pour afficher les éléments.
        a (int): Largeur ou position de référence pour l'affichage du texte.
        taille (int): Taille utilisée pour ajuster les dimensions du texte affiché.
        vies (int): Nombre actuel de vies du joueur avant la mise à jour.
        texte_vies: Référence à l'objet graphique représentant le texte des vies.

    Returns:
        tuple: (texte_vies, vies) - Référence mise à jour du texte des vies et le nouveau nombre de vies.
    """
    vies -= 1
    g.supprimer(texte_vies)
    if vies <= 0:
        texte_vies = g.afficherTexte(f"Vies: {0}", a + a // 4, taille * 2.5, "red", taille//2)
    elif vies == 2:
        texte_vies = g.afficherTexte(f"Vies: {vies}", a + a // 4, taille * 2.5, "orange", taille // 4)
    elif vies == 1:
        texte_vies = g.afficherTexte(f"Vie: {vies}", a + a // 4, taille * 2.5, "red", taille // 2)
    else:
        texte_vies = g.afficherTexte(f"Vies: {vies}", a + a // 4, taille * 2.5, "green", taille // 4)
    return  texte_vies, vies
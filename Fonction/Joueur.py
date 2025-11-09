#Joueur.py
from Fonction.Bombe import *
from Fonction.Upgrade import *
import sys

###############################################################################
# Section 2: Gestion du Joueur
###############################################################################

#########################
# Système de déplacement
#########################
def deplacement(g, perso, map_choix, taille, map_objet, tour, texte_tour, texte_score, texte_vies, a, score, vies, lv, tour_spawn_fantome, texte_lv, texte_portee_bombe):
    """
    Gère le déplacement du joueur et les interactions avec l'environnement, y compris les collisions,
    les upgrades, la gestion des fantômes et des bombes, ainsi que la mise à jour des tours.

    Args:
        g: Instance de la fenêtre graphique utilisée pour les affichages.
        perso: Objet représentant le joueur.
        map_choix (list): Matrice représentant la carte du jeu.
        taille (int): Taille d'une tuile dans le jeu.
        map_objet (list): Liste des objets présents sur la carte.
        tour (int): Nombre de tours restants avant la fin de la partie.
        texte_tour: Objet texte affichant le nombre de tours restants.
        texte_score: Objet texte affichant le score du joueur.
        texte_vies: Objet texte affichant le nombre de vies restantes.
        a (int): Largeur de la zone de jeu utilisée pour positionner les éléments graphiques.
        score (int): Score actuel du joueur.
        vies (int): Nombre de vies restantes.
        lv (int): Niveau actuel du jeu.
        tour_spawn_fantome (int): Intervalle en tours entre chaque apparition d'un fantôme.
        texte_lv: Objet texte affichant le niveau actuel.
        texte_portee_bombe: Objet texte affichant la portée actuelle des bombes.

    Returns:
        tuple: (score, vies) mis à jour après les déplacements et interactions.

    Fonctionnement:
        - Capture les mouvements du joueur via les touches directionnelles et applique les déplacements.
        - Gère les collisions avec les fantômes, les obstacles, et les objets ramassables.
        - Met à jour les éléments graphiques en fonction de l'état du jeu (score, vies, niveau, tours restants).
        - Incrémente et vérifie les états des bombes (explosion, nettoyage des effets).
        - Gère les déplacements des fantômes et leur apparition en fonction du nombre de tours de spawn fantomes.
        - Arrête le jeu si le joueur appuie sur "espace".
    """
    effets_explosion = [] # liste contenant les effets des explosions
    objet_non_passable = ["C", "M", "E"] # Objet considérer comme bloquant
    move_possible = ["b", "up", "down", "left", "right"] # touche possible du joueur
    tour_fantomes = 0
    tour_couleur = tour # Utile pour changé la couleur du titre en fonction d'un coefficient du tour initial
    joueur_move = g.recupererTouche()

    while tour >= 1:
        if vies <= 0: # si la vie du joueur atteint 0 la partie s'arrête
            break
        if joueur_move:
            if joueur_move == "space":
                sys.exit("Arret du programme demandé")

            direction = None
            if joueur_move == "b":
                direction = "b"
            elif joueur_move == "Up":
                direction = "up"
            elif joueur_move == "Down":
                direction = "down"
            elif joueur_move == "Left":
                direction = "left"
            elif joueur_move == "Right":
                direction = "right"

            if direction in move_possible: # si la touche est dans les touches possibles du joueur
                action = False # Permet de vérifier si une action à été faites
                if direction == "b":
                    action = poser_bombe(g, perso, taille)
                else:
                    # Vérifier si la case suivante contient un fantôme
                    case_suivante = check_case(perso, taille, map_choix, direction)
                    if case_suivante == "F":
                        # Gérer la collision avec le fantôme
                        nouvelle_x, nouvelle_y = get_next_position(perso, taille, direction)
                        vies, texte_vies = ghost_collision(g, map_choix, nouvelle_x, nouvelle_y, vies,
                                                           texte_vies, taille, a)
                        update_matrice(perso, taille, map_choix, direction) # changement matrice
                        perso = dep_joueur(g, perso, taille, direction) # changement graphique
                        action = True
                    elif case_suivante not in objet_non_passable: # si une case de la direction voulu du joueur est disponible
                        update_matrice(perso, taille, map_choix, direction)
                        perso = dep_joueur(g, perso, taille, direction)
                        action = True

                # Vérification qu'une action a bien été faite
                if action:
                    # Vérification des upgrades après le déplacement
                    vies, lv,score, texte_score, texte_vies, texte_lv, texte_portee_bombe = verifier_upgrades(g, perso, taille, vies, lv, texte_lv, texte_vies, texte_portee_bombe, a, score, texte_score)

                    # Incrémentation des tours des bombes uniquement si l'action est réussie
                    for bombes in bombes_actives:
                        bombes['mouvements'] += 1
                        print("tour des bombes :", bombes['mouvements'])

                    # Nettoyage des effets après 1 move du joueur
                    [g.supprimer(effet) for effet in effets_explosion]

                    # Fait bouger les fantômes s'il y en as
                    vies, texte_vies, map_choix = move_fantome(g, map_choix, taille, vies, texte_vies, a)
                    # vérifie si un fantome doit spawn
                    tour_fantomes = fantomes(g, tour_fantomes, tour_spawn_fantome, taille, map_choix)

                    # vérifie si une bombe doit exploser
                    score, vies, texte_score, texte_vies = verifier_bombes(g, perso, map_choix, taille, map_objet,
                                                                           score, vies, lv,
                                                                           effets_explosion, texte_vies, a, texte_score)
                    matrice(map_choix) # Affiche la matrice dans la console

                    # Mise à jour du compteur de tours et couleur en fonction du nb de tour restant
                    tour,texte_tour = compteur_tours(g,a,taille,tour,texte_tour,tour_couleur)

        # Si une touche n'est pas pressé alors attendre une touche
        joueur_move = g.attendreTouche()
    return score, vies

def compteur_tours(g,a,taille,tour,texte_tour,tour_couleur):
    """
    Met à jour le compteur de tours et ajuste l'affichage visuel en fonction du nombre de tours restants.

    Args:
        g: Instance de la fenêtre graphique.
        a (int): Largeur de la zone de jeu.
        taille (int): Taille des éléments sur l'interface (en pixels).
        tour (int): Nombre actuel de tours restants.
        texte_tour: Objet texte affichant le nombre de tours sur l'interface.
        tour_couleur (int): Nombre de tours initial utilisé pour définir les seuils de changement de couleur.

    Returns:
        tuple: (tour, texte_tour) mise à jour des tours restants.
    """
    tour -= 1
    g.supprimer(texte_tour)
    if tour <= 5:
        texte_tour = g.afficherTexte(f"Left turn: {tour}", a + a // 4, taille // 2, "red",
                                     taille // 2)
    elif tour <= tour_couleur // 4:
        texte_tour = g.afficherTexte(f"Left turn: {tour}", a + a // 4, taille // 2, "red",
                                     taille // 4)
    elif tour <= tour_couleur // 2:
        texte_tour = g.afficherTexte(f"Left turn: {tour}", a + a // 4, taille // 2, "orange",
                                     taille // 4)
    else:
        texte_tour = g.afficherTexte(f"Left turn: {tour}", a + a // 4, taille // 2, "green",
                                     taille // 4)
    return tour,texte_tour

def check_case(perso, taille, map_choix, direction):
    """
    Vérifie le contenu de la case dans la direction spécifiée pour effectuer un déplacement.

    Args:
        perso: Objet représentant le joueur
        taille (int): Taille d'une tuile
        map_choix (list): Matrice de la map
        direction (str): Direction à vérifier ('up', 'down', 'left', 'right')

    Returns:
        str: Contenu de la case dans la direction spécifiée
    """
    x = perso.x // taille
    y = perso.y // taille

    if direction == "up":
        return map_choix[y - 1][x]
    elif direction == "down":
        return map_choix[y + 1][x]
    elif direction == "left":
        return map_choix[y][x - 1]
    elif direction == "right":
        return map_choix[y][x + 1]

def dep_joueur(g, perso, taille, direction):
    """
    Gère le déplacement graphique du joueur dans une direction donnée.

    Args:
        g: Instance de la fenêtre graphique
        perso: Objet représentant le joueur
        taille (int): Taille d'une tuile
        direction (str): Direction du déplacement ('up', 'down', 'left', 'right')

    Returns:
        Perso: Objet joueur mis à jour (potentiellement avec une nouvelle image)
    """
    if direction == "up":
        g.deplacer(perso, 0, -taille)
    elif direction == "down":
        g.deplacer(perso, 0, taille)
    elif direction == "left":
        x, y = perso.x, perso.y
        g.supprimer(perso)
        perso = g.afficherImage(x, y, "Image/Images_resize/Perso_gauche_resize.png")
        g.deplacer(perso, -taille, 0)
    elif direction == "right":
        x, y = perso.x, perso.y
        g.supprimer(perso)
        perso = g.afficherImage(x, y, "Image/Images_resize/Perso_droite_resize.png")
        g.deplacer(perso, taille, 0)
    return perso

def update_matrice(perso, taille, map_choix, direction):
    """
    Met à jour la matrice de la map après un déplacement du joueur.

    Args:
        perso: Objet représentant le joueur
        taille (int): Taille d'une tuile
        map_choix (list): Matrice de la map
        direction (str): Direction du déplacement
    """
    x = perso.x // taille
    y = perso.y // taille

    if direction == "up":
        map_choix[y][x], map_choix[y - 1][x] = map_choix[y - 1][x], map_choix[y][x]
    elif direction == "down":
        map_choix[y][x], map_choix[y + 1][x] = map_choix[y + 1][x], map_choix[y][x]
    elif direction == "left":
        map_choix[y][x], map_choix[y][x - 1] = map_choix[y][x - 1], map_choix[y][x]
    elif direction == "right":
        map_choix[y][x], map_choix[y][x + 1] = map_choix[y][x + 1], map_choix[y][x]

# Fonction utilitaire
def get_next_position(perso, taille, direction):
    """
    Calcule la position suivante en fonction de la direction.
    Utiliser pour la gestion des collisions du joueur avec les fantômes
    """
    x = perso.x // taille
    y = perso.y // taille

    if direction == "up":
        return x, y - 1
    elif direction == "down":
        return x, y + 1
    elif direction == "left":
        return x - 1, y
    elif direction == "right":
        return x + 1, y
    return x, y



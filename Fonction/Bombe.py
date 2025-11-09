#Bombe.py
from Fonction.Fantome import *
from Fonction.Map_fonction import *
from Fonction.variable_global import *

###############################################################################
# Section 4: Système de Bombes
###############################################################################

def peut_poser_bombe(x, y):
    """
    Vérifie si une bombe peut être posée à une position donnée.

    Args:
        x (int): Coordonnée X en unités de grille
        y (int): Coordonnée Y en unités de grille

    Returns:
        bool: True si une bombe peut être posée, False sinon
    """
    for bombe in bombes_actives:
        if bombe['x'] == x and bombe['y'] == y:
            return False
    return True


def poser_bombe(g, perso, taille):
    """
    Place une bombe à la position actuelle du joueur.

    Args:
        g: Instance de la fenêtre graphique
        perso: Objet représentant le joueur
        taille (int): Taille d'une tuile

    Returns:
        bool: True si la bombe a été posée avec succès, False sinon
    """
    bomb_x = perso.x // taille
    bomb_y = perso.y // taille

    if peut_poser_bombe(bomb_x, bomb_y):
        bomb_img = g.afficherImage(bomb_x * taille, bomb_y * taille,
                                   "Image/Images_resize/Bombe_resize.png")

        # mouvement -1 car lorsque l'on crée une bombe le mouvement augmente de 1
        # pour toutes les bombes actives mêmes s'elles qui vienne d'être posé
        bombes_actives.append({
            'x': bomb_x,
            'y': bomb_y,
            'image': bomb_img,
            'mouvements': -1
        })
        return True
    return False


def verifier_bombes(g, perso, map_choix, taille, map_objet, score, vies, lv, effets_explosion, texte_vies, a,
                    texte_score, fin_partie=False):
    """
    Vérifie l'état de toutes les bombes actives et déclenche leur explosion si nécessaire.

    Args:
        g (objet): Fenêtre graphique ou interface de jeu utilisée pour afficher et supprimer des éléments.
        perso (objet): Objet représentant le joueur.
        map_choix (list): Nom de la carte actuellement choisie.
        taille (int): Taille des éléments sur la carte (en pixels).
        map_objet (list): Liste représentant les objets sur la carte.
        score (int): Score actuel du joueur.
        vies (int): Nombre de vies restantes du joueur.
        lv (int): Niveau actuel du jeu.
        effets_explosion (list): Liste des effets d'explosion à appliquer.
        texte_vies (str): Texte représentant le nombre de vies dans l'interface.
        a (int): Paramètre supplémentaire lié aux effets ou comportements spécifiques (ex: délai, temps, etc.).
        texte_score (str): Texte représentant le nombre total de score dans l'interface.
        fin_partie (bool): Indique si c'est la fin de la partie. Par défaut, False.

    Returns:
        tuple: (score, vies, texte_score, texte_vies) met à jour la barre des scores
    """
    tour_bombes = 5  # Nombre de tours avant l'explosion d'une bombe
    # Copie la liste car on va la modifier pendant l'itération
    bombes_a_verifier = bombes_actives.copy()
    if fin_partie:
        fantome_verif = fantomes_actifs.copy()
        for fantome in fantome_verif:
            g.supprimer(fantome['image'])
            fantomes_actifs.remove(fantome)

    for bombe in bombes_a_verifier:
        if fin_partie or bombe['mouvements'] >= tour_bombes:
            # Si c'est la fin de la partie, on n'ajoute pas de score
            if fin_partie:
                # Version simplifiée de l'explosion sans score
                g.supprimer(bombe['image'])
                bombes_actives.remove(bombe)
            else:
                # Explosion normale pendant le jeu
                score, vies, texte_score, texte_vies = executer_explosion(g, bombe, taille, map_choix, map_objet, perso, score, vies, lv, effets_explosion, texte_vies, a, texte_score)

    return score, vies, texte_score, texte_vies


def executer_explosion(g, bombe, taille, map_choix, map_objet, perso, score, vies, lv, effets_explosion, texte_vies, a, texte_score):
    """
    Gère l'explosion d'une bombe dans les 4 directions avec une portée variable.

    Args:
        g: Instance de la fenêtre graphique.
        bombe (dict): Dictionnaire contenant les informations de la bombe.
        taille (int): Taille d'une tuile.
        map_choix (list): Matrice de la carte du jeu.
        map_objet (list): Liste des objets présents sur la carte.
        perso: Objet représentant le joueur.
        score (int): Score actuel du joueur.
        vies (int): Points de vie du joueur.
        lv (int): Niveau actuel du jeu.
        effets_explosion (list): Liste des effets d'explosion à afficher.
        texte_vies (str): Texte affichant les vies actuelles du joueur.
        a (int): Paramètre utilisé pour afficher le texte sur l'écran.
        texte_score (str): Texte affichant le score actuel du joueur.

    Returns:
        tuple: (score, vies, texte_score, texte_vies) mise à jour de la barre des scores
    """
    # Suppression de l'image de la bombe
    g.supprimer(bombe['image'])
    bombes_actives.remove(bombe)

    # Calcul de la portée en fonction du niveau
    portee_bombe = 1 + lv // 2
    bomb_x = bombe['x']
    bomb_y = bombe['y']

    # Vérification des fantômes à la position de la bombe
    score, texte_score = verifier_fantomes_tues(g, (bomb_x, bomb_y), map_choix, taille,score, texte_score, a)

    # Définition des 4 directions : haut, bas, gauche, droite
    directions = [
        (0, -1, "haut"),
        (0, 1, "bas"),
        (-1, 0, "gauche"),
        (1, 0, "droite")
    ]

    # Vérification pour chaque direction
    for dx, dy, direction in directions:
        for distance in range(1, portee_bombe + 1):
            nx = bomb_x + (dx * distance)
            ny = bomb_y + (dy * distance)

            # Vérification des upgrades à détruire
            upgrades_a_verifier = upgrades_actifs.copy()
            for upgrade in upgrades_a_verifier:
                if (upgrade['x'] == nx and upgrade['y'] == ny) or \
                        (upgrade['x'] == bomb_x and upgrade['y'] == bomb_y):
                    g.supprimer(upgrade['image'])
                    upgrades_actifs.remove(upgrade)

            # Vérification des fantômes pour chaque case touchée par l'explosion
            score, texte_score = verifier_fantomes_tues(g, (nx, ny), map_choix, taille,score, texte_score, a)

            # Vérification du contenu de la case
            case = map_choix[ny][nx]

            # Vérification de la présence du joueur
            joueur_x = perso.x // taille
            joueur_y = perso.y // taille
            if (joueur_x == nx and joueur_y == ny) or \
                    (joueur_x == bomb_x and joueur_y == bomb_y):
                texte_vies, vies = degats_compteur(g, a, taille, vies, texte_vies)
            # Si c'est un mur ou une prise ethernet, arrêt de la propagation
            if case == "C" or case == "E":
                break

            # Si c'est un mur destructible
            if case == "M":
                # Suppression du mur
                map_choix[ny][nx] = " "
                for obj in map_objet:
                    if obj.x == nx * taille and obj.y == ny * taille:
                        g.supprimer(obj)
                        map_objet.remove(obj)
                        score += 10
                        g.supprimer(texte_score)
                        texte_score = g.afficherTexte(f"Score: {score}", a + a // 4, taille * 1.5, "black", taille // 4)

            # Création de l'effet visuel
            if dx == 0:  # Explosion verticale
                effet = g.afficherImage(
                    bomb_x * taille,
                    ny * taille,
                    "Image/Images_resize/Explosion_extremite_resize.png")
            else:  # Explosion horizontale
                effet = g.afficherImage(
                    nx * taille,
                    bomb_y * taille,
                    "Image/Images_resize/Explosion_extremite_resize.png")
            effets_explosion.append(effet)

            for bombes in bombes_actives:
                if (nx == bombes['x']) and (ny == bombes['y']):
                    score, vies, texte_score, texte_vies = executer_explosion(g, bombes, taille, map_choix, map_objet, perso, score, vies, lv, effets_explosion, texte_vies, a, texte_score)

    # Centre de l'explosion (-4pv*portee de la bombe si joueur au milieu + si touché par autre bombes)
    centre = g.afficherImage(bomb_x * taille, bomb_y * taille, "Image/Images_resize/Explosion_centre_resize.png")
    effets_explosion.append(centre)

    return score, vies, texte_score, texte_vies
#Fantome.py
from Fonction.Joueur import *
from Fonction.variable_global import *
from Fonction.Map_fonction import *
import random

###############################################################################
# Section 3: Gestion des fantômes
###############################################################################

def fantomes(g, tour_fantomes, tour_spawn_fantome, taille, map_choix):
    """
    Gère le spawn des fantômes depuis les prises ethernet et met à jour la matrice de la carte.

    Args:
        g: Instance de la fenêtre graphique.
        tour_fantomes (int): Compteur de tours depuis le dernier spawn de fantômes.
        tour_spawn_fantome (int): Intervalle en tours entre chaque apparition de fantômes.
        taille (int): Taille d'une tuile (en pixels).
        map_choix (list): Matrice représentant la carte de jeu.

    Returns:
        tuple: (tour_fantomes, map_choix) mis à jour après le traitement du spawn des fantômes.
    """
    tour_fantomes += 1

    # Vérifie si c'est le moment de faire apparaître des fantômes
    if tour_fantomes % tour_spawn_fantome == 0:
        # Trouve toutes les prises ethernet
        prises = count_ethernet_prises(map_choix)

        # Pour chaque prise ethernet
        for x, y in prises:
            spawn_directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(spawn_directions)

            # Essaie chaque direction possible
            for dx, dy in spawn_directions:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < len(map_choix[0]) and 0 <= new_y < len(map_choix):
                    if map_choix[new_y][new_x] == " ":  # Vérifie si la case est libre
                        # Spawn un fantôme
                        fantome_img = g.afficherImage(new_x * taille, new_y * taille,
                                                      "Image/Images_resize/Fantome_resize.png")

                        # Ajoute le fantôme à la liste des fantômes actifs
                        fantomes_actifs.append({
                            'x': new_x,
                            'y': new_y,
                            'image': fantome_img
                        })

                        map_choix[new_y][new_x] = "F"  # Marque la présence du fantôme dans la matrice
                        break

    return tour_fantomes

def move_fantome(g, map_choix, taille, vies, texte_vies, a):
    """
    Gère les déplacements des fantômes sur la carte et leur interaction avec le joueur.

    Args:
        g: Instance de la fenêtre graphique.
        map_choix (list): Matrice représentant la carte de jeu.
        taille (int): Taille d'une tuile (en pixels).
        vies (int): Nombre de vies restantes du joueur.
        texte_vies: Objet texte représentant les vies du joueur dans l'interface.
        a (int): Largeur de la zone de jeu, utilisé pour les calculs graphiques.

    Returns:
        tuple: (vies, texte_vies, map_choix) mis à jour après le déplacement des fantômes et les interactions.
    """
    # Copie la liste car on va potentiellement la modifier pendant l'itération
    fantomes_a_deplacer = fantomes_actifs.copy()

    for fantome in fantomes_a_deplacer:
        # Position actuelle du fantôme
        fx = fantome['x']
        fy = fantome['y']

        # Trouve les cases disponibles pour le mouvement
        moves = get_available_moves(map_choix, fx, fy)

        # Vérifie si le fantôme est adjacent au joueur
        if est_adjacent(fx, fy, map_choix):
            # Inflige des dégâts si adjacent
            texte_vies, vies = tue_fantome(g, a, taille, vies, texte_vies, fantome, map_choix)
            return vies, texte_vies, map_choix

        if moves:
            # Si plus d'un mouvement est disponible, on choisit aléatoirement
            if len(moves) > 1:
                # Retire la position précédente si elle existe
                if 'previous_pos' in fantome:
                    moves = [m for m in moves if m != fantome['previous_pos']]

                new_x, new_y = random.choice(moves)
            else:
                # Sinon, on prend le seul mouvement disponible ancienne position
                new_x, new_y = moves[0]

            # Mise à jour des positions du fantôme
            update_fantome_position(fantome, fx, fy, new_x, new_y, map_choix, g, taille)

    return vies, texte_vies, map_choix


def update_fantome_position(fantome, fx, fy, new_x, new_y, map_choix, g, taille):
    """
    Met à jour la position du fantôme dans la matrice et graphiquement.

    Args:
        fantome: Dictionnaire représentant le fantôme.
        fx: Position actuelle du fantôme (horizontal).
        fy: Position actuelle du fantôme (vertical).
        new_x: Nouvelle position du fantôme (horizontal).
        new_y: Nouvelle position du fantôme (vertical).
        map_choix (list): Matrice représentant la carte de jeu.
        g: Instance de la fenêtre graphique.
        taille (int): Taille d'une tuile (en pixels).
    """
    # Sauvegarde la position actuelle comme position précédente
    fantome['previous_pos'] = (fx, fy)

    # Met à jour la matrice
    map_choix[fy][fx] = " "  # Efface l'ancienne position
    map_choix[new_y][new_x] = "F"  # Marque la nouvelle position

    # Met à jour les coordonnées du fantôme
    fantome['x'] = new_x
    fantome['y'] = new_y

    # Déplace le fantôme graphiquement
    g.deplacer(fantome['image'], (new_x - fx) * taille, (new_y - fy) * taille)

def get_available_moves(map_choix, x, y):
    """
    Trouve toutes les cases disponibles pour le mouvement du fantome.

    Args:
        map_choix (list): Matrice de la map
        x : Position actuelle (horizontal)
        y : Position actuelle (vertical)

    Returns:
        moves (list): Liste des positions disponibles [(x, y), ...]
    """
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Bas, Droite, Haut, Gauche
    moves = []

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < len(map_choix[0]) and 0 <= new_y < len(map_choix):
            if map_choix[new_y][new_x] == " ":  # Vérifie si la case est libre
                moves.append((new_x, new_y))

    return moves

def count_ethernet_prises(map_choix):
    """
    Compte et localise les prises ethernet sur la map
    afin d'avoir un fantome par prise ethernet.

    Args:
        map_choix (list): Matrice de la map

    Returns:
        prises (list): Liste des positions des prises ethernet [(x, y), ...]
    """
    prises = []
    for y in range(len(map_choix)):
        for x in range(len(map_choix[0])):
            if map_choix[y][x] == "E":
                prises.append((x, y))
    return prises

# Vérifie si un fantome est tué gestion des upgrades
def verifier_fantomes_tues(g, fantome_pos, map_choix,taille,score,texte_score,a):
    """
    Vérifie si des fantômes sont touchés par une explosion et gère leur suppression ainsi que
    la création d'upgrades.

    Args:
        g: Instance de la fenêtre graphique.
        fantome_pos (tuple): Coordonnées (x, y) de l'explosion.
        map_choix (list): Matrice représentant la carte de jeu.
        taille (int): Taille d'une tuile (en pixels).
        score (int): Score actuel du joueur.
        texte_score: Objet texte affichant le score actuel dans l'interface.
        a (int): Largeur de la zone de jeu, utilisé pour positionner les textes graphiques.

    Returns:
        tuple: (score, texte_score) mis à jour après la suppression des fantômes et la création d'upgrades.
    """
    fantomes_a_verifier = fantomes_actifs.copy()
    for fantome in fantomes_a_verifier:
        if fantome['x'] == fantome_pos[0] and fantome['y'] == fantome_pos[1]:
            # ajoute 2 au score:
            score += 100
            g.supprimer(texte_score)
            texte_score = g.afficherTexte(f"Score: {score}", a + a // 4, taille * 1.5, "black", taille // 4)

            # Supprime le fantôme graphiquement
            g.supprimer(fantome['image'])
            # Retire le fantôme de la liste des fantômes actifs
            fantomes_actifs.remove(fantome)
            # Met à jour la matrice
            map_choix[fantome_pos[1]][fantome_pos[0]] = " "  # Marque la présence d'un upgrade
            # Crée un upgrade à la position du fantôme tué
            upgrade_img = g.afficherImage(
                fantome_pos[0] * taille,
                fantome_pos[1] * taille,
                "Image/Images_resize/Upgrade_resize.png"
            )
            # Ajoute l'upgrade à la liste des upgrades actifs
            upgrades_actifs.append({
                'x': fantome_pos[0],
                'y': fantome_pos[1],
                'image': upgrade_img
            })
    return score,texte_score



def tue_fantome(g, a, taille, vies, texte_vies,fantome,map_choix):
    """
    Gère la suppression d'un fantôme après qu'il ait touché le joueur.
    Cette fonction inflige des dégâts au joueur, met à jour le nombre de vies et
    retire le fantôme de la carte (matrice et graphique) et de la liste des fantômes actifs.

    Args:
        g: Instance de la fenêtre graphique.
        a (int): Largeur de la zone de jeu, utilisé pour positionner les textes graphiques.
        taille (int): Taille d'une tuile (en pixels).
        vies (int): Nombre de vies restantes du joueur avant la collision.
        texte_vies: Objet texte affichant le nombre de vies dans l'interface graphique.
        fantome (dict): Dictionnaire contenant les informations du fantôme, y compris sa position et son image.
        map_choix (list): Matrice représentant la carte du jeu.

    Returns:
        tuple: (texte_vies, vies) mis à jour après avoir infligé des dégâts et supprimé le fantôme.
    """
    fx = fantome['x']
    fy = fantome['y']
    texte_vies, vies = degats_compteur(g, a, taille, vies, texte_vies)
    map_choix[fy][fx] = " "
    g.supprimer(fantome['image'])
    fantomes_actifs.remove(fantome)
    return texte_vies, vies




## Collision au Joueur
def ghost_collision(g, map_choix, x, y, vies, texte_vies, taille, a):
    """
    Gère la collision avec un fantôme lorsque le joueur se déplace et entre en contact avec un fantôme.
    Cette fonction est utilisée lorsqu'un joueur fonce directement sur un fantôme ou est bloqué par celui-ci.

    Args:
        g: Instance de la fenêtre graphique.
        map_choix (list): Matrice représentant la carte du jeu.
        x (int): Coordonnée x de la position du joueur.
        y (int): Coordonnée y de la position du joueur.
        vies (int): Nombre de vies restantes du joueur avant la collision.
        texte_vies: Objet texte affichant le nombre de vies dans l'interface graphique.
        taille (int): Taille d'une tuile (en pixels).
        a (int): Largeur de la zone de jeu, utilisé pour la position du texte dans l'interface.

    Returns:
        tuple: (vies, texte_vies) mis à jour après la collision avec un fantôme.
    """
    # Trouve et supprime le fantôme à cette position
    fantomes_a_verifier = fantomes_actifs.copy()
    for fantome in fantomes_a_verifier:
        if fantome['x'] == x and fantome['y'] == y:
            g.supprimer(fantome['image'])
            fantomes_actifs.remove(fantome)
            map_choix[y][x] = " "

    # Réduit les points de vie du joueur
    texte_vies, vies = degats_compteur(g, a, taille, vies, texte_vies)
    return vies, texte_vies

def est_adjacent(fx, fy,map_choix):
    """
    Vérifie si un fantôme est adjacent à un joueur (en haut, bas, gauche, ou droite).

    Args:
        fx (int): Coordonnée x de la position du fantôme.
        fy (int): Coordonnée y de la position du fantôme.
        map_choix (list): Matrice représentant la carte du jeu.

    Returns:
        bool: True si le fantôme est adjacent à un joueur ('P'), False sinon.
    """
    # Vérification des cases adjacentes (haut, droite, bas, gauche)
    return (map_choix[fy+1][fx] == "P") or \
           (map_choix[fy][fx+1] == "P") or \
           (map_choix[fy-1][fx] == "P") or \
           (map_choix[fy][fx-1] == "P")
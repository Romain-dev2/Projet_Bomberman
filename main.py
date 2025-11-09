# main.py
from tkiteasy import ouvrirFenetre
# Images
from Image.Images import*
# Fonction
from Fonction.Joueur import *
from Fonction.Bombe import *
from Fonction.Upgrade import *

def verifier_victoire(map_choix):
    """
    Vérifie si toutes les conditions de victoire sont remplies.

    Args:
        map_choix (list): Matrice de la map

    Returns:
        bool: True si le joueur a gagné, False sinon
    """
    for y in range(len(map_choix)):
        for x in range(len(map_choix[0])):
            if map_choix[y][x] == "M":  # S'il reste des murs destructibles
                return False
    return True

def get_initial_map(map_name):
    """
    Récupère une copie de la map et ses paramètres.

    Args:
        map_name (str): Nom de la map à charger (ex: 'map_1')

    Returns:
        tuple: (map_matrice, tours, tour_fantome)
    """
    from Fonction.map import all_maps
    maps = all_maps()
    if map_name in maps:
        map_function = maps[map_name]['function']
        return map_function()
    else:
        raise ValueError(f"Map '{map_name}' introuvable.")

def reset_game_state():
    """
    Réinitialise toutes les variables globales du jeu.
    À appeler au début de chaque partie.
    """
    global bombes_actives,fantomes_actifs
    bombes_actives = []
    fantomes_actifs = []

def partie(map_name=None):
    """
    Gère une partie complète du jeu.

    Args:
        map_name: Nom de la map à utiliser (si None, demande à l'utilisateur)

    Returns:
        tuple: (resultat, map_name) - Résultat de la partie et nom de la map utilisée
    """
    # Réinitialisation de l'état du jeu
    reset_game_state()
    map_objet = []

    # Sélection de la map
    if map_name is None:
        maps = affichage_map()  # Affiche les maps disponibles et retourne la liste des tuples (identifiant, titre)
        choix,map_choix, tours, tour_spawn_fantome = select_map(maps)  # Appelle la fonction select_map
        map_name = maps[choix - 1][0]  # Met à jour le nom de la map sélectionnée

    # Récupération d'une copie fraîche de la map
    map_choix, tour, tour_spawn_fantome = get_initial_map(map_name)
    taille = taille_map(map_choix)

    # Dimension de la fenêtre
    a = len(map_choix[0]) * taille
    b = len(map_choix) * taille
    # Ouverture fenêtre
    g = ouvrirFenetre(a * 1.5, b)
    # permet d'avoir le focus de la fenêtre lors du relancement de la map
    g.focus_force()
    g.update()

    # Redimensionner les images
    images_resize(taille)

    ## Affichage dans la console
    print(f"Dimensions de la carte : {a}x{b}px")
    print(f"Taille des tuiles : {taille}")
    print(f"Tour fantome: {tour_spawn_fantome}")
    matrice(map_choix)

    # Création de la map
    perso, ethernet = creation_map(g,a,b, map_choix, taille, map_objet)

    ## Initialisation des variables de jeu
    # Tour et tours_spawn_fantome sont données avec la map
    score = 0
    vies = 3
    lv = 0
    portee_bombe = 1

    # Interface du jeu
    texte_vies, texte_score, texte_tour, texte_lv, texte_portee_bombe = barre_score(g, taille, a,b, score, vies, lv,tour,portee_bombe)

    # Boucle de jeu principale
    if perso and ethernet:
        g.focus_set() # permet d'avoir le focus en relançant le jeu
        score, vies = deplacement(g, perso, map_choix, taille, map_objet, tour,
                                  texte_tour,texte_score,texte_vies, a, score, vies, lv,
                                  tour_spawn_fantome,texte_lv, texte_portee_bombe)

        # Nettoyage des bombes restantes
        effets_explosion = []
        score, vies, texte_score, texte_vies = verifier_bombes(g, perso, map_choix, taille,
                                                               map_objet, score, vies, lv,
                                                               effets_explosion, texte_vies,
                                                               a, texte_score, fin_partie=True)
    else:
        sys.exit("Aucun personnage ou aucune prise ethernet n'est présent")

    resultat = verifier_victoire(map_choix)
    g.fermerFenetre()

    return resultat, map_name, score


def ecran_fin(resultat, score):
    """
    Affiche l'écran de fin de partie et gère les options de redémarrage.

    Args:
        resultat (bool): True si victoire, False si défaite
        score (int): Score final du joueur

    Returns:
        str: Action choisie par le joueur ('restart' ou 'quit')
    """
    # Taille idéal préalablement calculer
    a, b = 750, 550
    g = ouvrirFenetre(a, b)
    g.focus_force()
    g.dessinerRectangle(0, 0, a * 1.5, b + 50, "white")

    # Affichage du résultat
    if resultat:
        g.afficherTexte("YOU WIN", a // 2, b // 2, "green", 50)
    else:
        g.afficherTexte("GAME OVER", a // 2, b // 2, "red", 50)

    # Affichage du score
    g.afficherTexte(f"Your score: {score}", a // 2, b // 2 - 50, "gray", 20)

    # Instructions pour le joueur
    g.afficherTexte("Press 'r' to restart", a // 2, b - 100, "gray", 20)
    g.afficherTexte("Press 'space' to quit", a // 2, b - 70, "gray", 20)

    # Tant qu'une touche n'est pas pressé alors attendre une touche
    while True:
        touche = g.attendreTouche()
        if touche == "space":
            g.fermerFenetre()
            return "quit"
        elif touche == "r":
            g.fermerFenetre()
            return "restart"


def main():
    """Fonction principale du jeu gérant la boucle de redémarrage"""
    current_map = None

    while True:
        # Joue une partie
        resultat, last_map, score = partie(current_map)

        # Affiche l'écran de fin et attend l'action du joueur
        action = ecran_fin(resultat, score)

        if action == "quit":
            break # arrêt du programme
        elif action == "restart":
            current_map = last_map  # Garde la même map pour le redémarrage

if __name__ == "__main__":
    main()
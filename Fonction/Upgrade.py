#Upgrade.py
from Fonction.variable_global import *
from Fonction.Map_fonction import *

###############################################################################
# Section 5: Gestion des Upgrades
###############################################################################

def verifier_upgrades(g, perso, taille, vies, lv, texte_lv, texte_vies, texte_portee_bombe, a, score, texte_score):
    """
    Vérifie si le joueur ramasse un upgrade et applique ses effets.

    Args:
        g: Instance de la fenêtre graphique.
        perso: Objet représentant le joueur.
        taille: Taille d'une tuile.
        vies: Points de vie actuels du joueur.
        lv: Niveau actuel du joueur.
        texte_lv: Texte représentant le niveau affiché à l'écran.
        texte_vies: Texte représentant les vies affichées à l'écran.
        texte_portee_bombe: Texte représentant la portée de la bombe affichée à l'écran.
        a: Largeur de la fenêtre graphique (utilisé pour l'affichage).
        score: Score actuel du joueur.
        texte_score: Texte représentant le score affiché à l'écran.

    Returns:
        tuple: (vies, lv,score, texte_score, texte_vies, texte_lv, texte_portee_bombe) mis à jour dans la barre des scores
    """
    joueur_x = perso.x // taille
    joueur_y = perso.y // taille

    upgrades_a_verifier = upgrades_actifs.copy()
    for upgrade in upgrades_a_verifier:
        if upgrade['x'] == joueur_x and upgrade['y'] == joueur_y:
            # Supprime l'upgrade graphiquement
            g.supprimer(upgrade['image'])
            # Retire l'upgrade de la liste des upgrades actifs
            upgrades_actifs.remove(upgrade)

            # Augmente le niveau
            lv += 1
            score += 20  # Ajout du point pour avoir ramassé l'upgrade
            g.supprimer(texte_score)
            texte_score = g.afficherTexte(f"Score: {score}", a + a // 4, taille * 1.5, "black", taille // 4)
            g.supprimer(texte_lv)
            texte_lv = g.afficherTexte(f"Lv: {lv}",
                                       a + a // 4,
                                       taille * 3.5,
                                       "black",
                                       taille // 4)

            # Applique les effets en fonction du niveau
            if lv % 2 == 0:  # Niveaux pairs : augmentation de la portée
                g.supprimer(texte_portee_bombe)
                portee_bombe = 1 + lv // 2
                texte_portee_bombe = g.afficherTexte(
                    f"Portée bombe: {portee_bombe}",
                    a + a // 4,
                    taille * 4.5,
                    "black",
                    taille // 4
                )
            else:  # Niveaux impairs : +1 PV
                # vies +2 car la fonction fait -1 donc +2-1 = +1
                texte_vies, vies = degats_compteur(g, a, taille, vies+2, texte_vies)

    return vies, lv,score, texte_score, texte_vies, texte_lv, texte_portee_bombe
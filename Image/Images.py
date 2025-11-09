# Images.py
from PIL import Image

# Images :
Perso_droite = Image.open("Image/Images_default/Perso_droite.png")
Perso_gauche = Image.open("Image/Images_default/Perso_gauche.png")
Colonne = Image.open("Image/Images_default/colonne.png")
Mur = Image.open("Image/Images_default/mur.png")
Fantome = Image.open("Image/Images_default/fantome.png")
Ethernet = Image.open("Image/Images_default/ethernet.png")
Bombe = Image.open("Image/Images_default/bombe.png")
Upgrade = Image.open("Image/Images_default/upgrade.png")
Explosion_extremite = Image.open("Image/Images_default/explosion_extremite.png")
Explosion_centre = Image.open("Image/Images_default/explosion_centre.png")

# Redimensions des images
def images_resize(taille):
    """
    Redimensionne les images à la taille calculé et les sauvegarde dans un autre répertoire.

    Args:
        taille (int): La nouvelle taille (en pixels) pour redimensionner les images.
    """
    Perso_droite.resize((taille,taille)).save("Image/Images_resize/Perso_droite_resize.png")
    Perso_gauche.resize((taille,taille)).save("Image/Images_resize/Perso_gauche_resize.png")
    Colonne.resize((taille,taille)).save("Image/Images_resize/Colonne_resize.png")
    Mur.resize((taille,taille)).save("Image/Images_resize/Mur_resize.png")
    Fantome.resize((taille,taille)).save("Image/Images_resize/Fantome_resize.png")
    Ethernet.resize((taille,taille)).save("Image/Images_resize/Ethernet_resize.png")
    Bombe.resize((taille,taille)).save("Image/Images_resize/Bombe_resize.png")
    Upgrade.resize((taille,taille)).save("Image/Images_resize/Upgrade_resize.png")
    Explosion_extremite.resize((taille,taille)).save("Image/Images_resize/Explosion_extremite_resize.png")
    Explosion_centre.resize((taille,taille)).save("Image/Images_resize/Explosion_centre_resize.png")
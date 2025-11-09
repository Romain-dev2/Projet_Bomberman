from tkiteasy import ouvrirFenetre
from PIL import Image
# Ouverture de fenêtre
a = 700
b = 700

###################
# liste :
map = ["CCCCCCCCC",
       "C  P    C",
       "CMCMCMCMC",
       "CMMMM E C",
       "CCCCCCCCC",
       ]

map_objet = []

################
# Cooordonnées :
y,x = len(map),len(map[0])

px_largeur = a//x
px_hauteur = b//y
print(px_largeur,px_hauteur)
if px_largeur > px_hauteur:
    px_largeur = px_hauteur
else:
    px_hauteur = px_largeur

g = ouvrirFenetre(x*px_largeur +200, y*px_hauteur)
g.dessinerRectangle(x*px_largeur,0,200+10,b+10,"white")
#max_height = g.winfo_screenheight()
#max_width = g.winfo_screenwidth()

################
#Images :
Image.open("../images/colonne.png").resize((px_largeur, px_hauteur)).save("../images/colonne_jsp.png")
Image.open("../images/perso.png").resize((px_largeur, px_hauteur)).save("../images/perso_jsp.png")
Image.open("../images/mur.png").resize((px_largeur, px_hauteur)).save("../images/mur_jsp.png")
Image.open("../images/ethernet.png").resize((px_largeur, px_hauteur)).save("../images/ethernet_jsp.png")

################
# map :
for ordonnée in range(y):
    map_objet.append([])
    for abscisse in range(x):
        if map[ordonnée][abscisse] == "C":
            colonne = g.afficherImage(abscisse*px_largeur, ordonnée*px_hauteur,"images/colonne_jsp.png")
            map_objet[ordonnée].append(colonne)
        elif map[ordonnée][abscisse] == "P":
            joueur = g.afficherImage(abscisse * px_largeur, ordonnée * px_hauteur, "images/perso_jsp.png")
            map_objet[ordonnée].append(joueur)
            joueur_temp = [abscisse,ordonnée]
        elif map[ordonnée][abscisse] == "M":
            mur = g.afficherImage(abscisse * px_largeur, ordonnée * px_hauteur, "images/mur_jsp.png")
            map_objet[ordonnée].append(mur)
        elif map[ordonnée][abscisse] == "E":
            ethernet = g.afficherImage(abscisse * px_largeur, ordonnée * px_hauteur, "images/ethernet_jsp.png")
            map_objet[ordonnée].append(ethernet)
        else:
            map_objet[ordonnée].append("#")

###########################################################
# Affichage de la matrice dans la console (coordonnée (x,y):
print(end="  ")
for j in range(1,len(map[0])+1):
    print(j,end="")
print()
for i in range(1,len(map)+1):
    print(i,map[i-1])

###########################################################
# Mouvement du joueur


joueur = map_objet[joueur_temp[0]][joueur_temp[1]]
touche = g.attendreTouche()
while g.attendreTouche() != "space":
    if touche:
        if touche == "Up" :
            print('UP')
            g.deplacer(joueur,70,70)
        elif touche == "Down":
            print('DOWN')
        elif touche == "Left" :
            print('LEFT')
        elif touche == "Right" :
            print('RIGHT')
    touche = g.recupererTouche()


#######################################
# Touche pour mettre fin au jeux
g.fermerFenetre()
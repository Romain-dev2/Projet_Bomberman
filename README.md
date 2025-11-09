# 💣 Bomberman Tour par Tour

> Une réinterprétation stratégique du classique Bomberman en tour par tour, développée en Python avec Tkinter

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)

## 🎮 Présentation

Ce projet est un **jeu Bomberman en tour par tour** où la stratégie rencontre l'action. Les joueurs doivent détruire tous les murs destructibles dans un nombre limité de tours tout en survivant aux attaques de fantômes et en gérant soigneusement les explosions de bombes.

**Caractéristiques principales :**
- ✨ Gameplay stratégique au tour par tour
- 👻 Système d'apparition dynamique de fantômes
- 💎 Système d'améliorations progressives
- 🗺️ Plusieurs cartes avec différents niveaux de difficulté
- 🎯 Suivi des scores et gestion des vies
- ⛓️ Mécaniques d'explosions en chaîne

## 📸 Captures d'écran

*À venir - Les captures d'écran du gameplay seront ajoutées ici*

## 🎯 Objectifs du Jeu

### Conditions de Victoire
- Détruire tous les murs destructibles (caisses) sur la carte
- Survivre jusqu'à ce que le compteur de tours atteigne zéro
- Maximiser votre score !

### Conditions de Défaite
- Épuiser toutes vos vies (PV atteint 0)
- Échec à détruire tous les murs avant la fin des tours

## 🕹️ Comment Jouer

### Contrôles
| Touche | Action |
|--------|--------|
| ⬆️ ⬇️ ⬅️ ➡️ | Déplacer le joueur |
| `B` | Poser une bombe |
| `Espace` | Quitter la partie (à tout moment) |
| `R` | Redémarrer (après fin de partie) |

### Mécaniques de Jeu

#### Système de Tours
Chaque action consomme **1 tour** :
- Se déplacer dans n'importe quelle direction
- Poser une bombe

#### Système de Score
| Action | Points |
|--------|--------|
| Détruire un mur | +10    |
| Récolter une amélioration | +20    |
| Tuer un fantôme avec une bombe | +100   |

#### Gestion de la Santé
- **-1 PV** : Attaque de fantôme ou bord d'explosion
- **-x explosion PV** : Explosions simultanées multiples
- **Mort instantanée** : Être au centre d'une explosion de bombe (zone rouge)

#### Système de Fantômes
- Les fantômes apparaissent depuis les prises Ethernet (`E`) tous les N tours
- Ils se déplacent aléatoirement après chaque action du joueur
- Évitent de revenir sur leur position précédente quand possible
- Attaquent au contact, puis disparaissent
- Laissent des améliorations quand ils sont tués par des bombes

#### Améliorations (Power-Ups)
Système d'amélioration progressive basé sur le niveau du joueur :
- **Niveau 1** : +1 Vie
- **Niveau 2** : +1 Portée de Bombe
- **Niveau 3** : +1 Vie
- Le cycle continue...

#### Mécaniques d'Explosion
- **Réactions en Chaîne** : Les bombes déclenchent les bombes à proximité de manière récursive
- **Affichage en Deux Phases** : 
  1. Centre rouge (zone de mort instantanée)
  2. Quatre rayons directionnels
- Portée affectée par les améliorations
- Détruit les murs, tue les fantômes et affecte le joueur

## 🗺️ Cartes

Le jeu inclut trois cartes avec difficulté croissante :

| Carte | Difficulté | Description |
|-------|-----------|-------------|
| Carte 1 | Facile | Petite carte tutoriel |
| Carte 2 | Moyenne | Disposition standard avec obstacles modérés |
| Carte 3 | Difficile | Grande carte avec nombreux obstacles |

Chaque carte possède des paramètres prédéfinis :
- Nombre total de tours
- Fréquence d'apparition des fantômes
- Complexité du niveau

## 🛠️ Détails Techniques

### Structure du Projet
```
bomberman-game/
│
├── main.py                 # Boucle principale et point d'entrée
├── tkiteasy.py            # Wrapper Tkinter pour graphismes simplifiés
├── .gitignore             # Règles d'exclusion Git
│
├── Fonction/              # Modules de logique du jeu
│   ├── Joueur.py         # Mécaniques du joueur
│   ├── Bombe.py          # Système de bombes
│   ├── Upgrade.py        # Système d'améliorations
│   └── Map_list.py       # Définitions des cartes
│
└── Image/                 # Ressources graphiques
    ├── Images/           # Images originales
    └── Images_resize/    # Images redimensionnées dynamiquement
```

### Technologies Utilisées
- **Python 3.x** : Langage de programmation principal
- **Tkinter** : Framework d'interface graphique
- **PIL/Pillow** : Traitement et manipulation d'images
- **tkiteasy** : Wrapper personnalisé pour simplifier l'utilisation de Tkinter

### Fonctionnalités Clés Implémentées
- **Redimensionnement Dynamique des Images** : Ajustement automatique selon la taille de l'écran
- **Conception Orientée Objet** : Structure de code modulaire
- **Architecture Événementielle** : Gestion réactive des entrées clavier
- **Algorithmes Récursifs** : Mécaniques d'explosions en chaîne

## 📦 Installation

### Prérequis
```bash
# Python 3.12 requis
python --version
```

### Dépendances
```bash
# Installer les packages requis
pip install pillow
```

### Configuration
```bash
# Cloner le dépôt
git clone https://github.com/votreusername/bomberman-tourpartour.git

# Naviguer dans le répertoire du projet
cd bomberman-tourpartour

# Lancer le jeu
python main.py
```

## 🎮 Déroulement d'une Partie

1. **Sélection de Carte** : Choisir parmi 3 cartes disponibles (ou appuyer sur 0 pour quitter)
2. **Début de Partie** : La fenêtre s'ouvre avec la carte sélectionnée
3. **Jeu Stratégique** : Planifier les mouvements avec soin, tours limités
4. **Écran de Fin** : Affichage du score final et options
5. **Option de Redémarrage** : Appuyer sur `R` pour rejouer la même carte ou `Espace` pour quitter

## 🧩 Éléments du Jeu

### Symboles de la Carte
- `P` : Position de départ du joueur
- `M` : Murs destructibles (caisses)
- `I` : Murs indestructibles
- `E` : Prises Ethernet (points d'apparition des fantômes)
- ` ` : Espace vide praticable

## 💡 Conseils Stratégiques

1. **Planifier à l'Avance** : Avec des tours limités, chaque mouvement compte
2. **Placement de Bombes** : Utiliser les réactions en chaîne pour plus d'efficacité
3. **Gestion des Fantômes** : Suivre le timing d'apparition
4. **Priorité aux Améliorations** : Équilibrer les améliorations de vie et de portée
5. **Zones de Sécurité** : Toujours avoir une voie d'évacuation depuis vos bombes
6. **Danger du Centre** : Ne jamais rester au centre d'une bombe - mort instantanée !

## 🔮 Améliorations Futures

- [ ] Cartes additionnelles et niveaux de difficulté
- [ ] Mode multijoueur
- [ ] Sauvegarde/Chargement de parties
- [ ] Effets sonores et musique
- [ ] Contrôles personnalisables
- [ ] Système de classement
- [ ] Amélioration des animations

## 👥 Auteurs

**Romain MESSAGER & Zyed TARCHOUN**  
Étudiants en 2ᵉ année de BUT Informatique – IUT de Vélizy (UVSQ)  
🔗 [GitHub – Romain-dev2](https://github.com/Romain-dev2)
# Map.py
def map1():
    """
    Map 1 - Niveau exemple

    Returns:
        tuple: (map_1,tour,tour_spawn_fantome)
    """
    map_1 = [
        list("CCCCCCCCCCCCC"),
        list("CP          C"),
        list("CMCMCMC C C C"),
        list("CMMMM   MMMMC"),
        list("CMCMCMC C C C"),
        list("CMMMM      EC"),
        list("CCCCCCCCCCCCC"),
    ]
    tour = 120
    tour_spawn_fantome = 20
    return map_1, tour, tour_spawn_fantome

def map2():
    """
    Map 2 - Niveau facile

    Returns:
            tuple: (map_1,tour,tour_spawn_fantome)
    """
    map_2 = [
        list("CCCCCCCCCCCCCCCCCCC"),
        list("CP                C"),
        list("CMCMCMCMC CMC CMC C"),
        list("CMM M       MMMM  C"),
        list("CMCMCMC CMC CMCMC C"),
        list("CMMMM      MMMM   C"),
        list("CMCMCMCMCMCMCMCMC C"),
        list("CMMMM  MM  MM M  EC"),
        list("CCCCCCCCCCCCCCCCCCC"),
    ]
    tour = 240
    tour_spawn_fantome = 20
    return map_2, tour, tour_spawn_fantome

def map3():
    """
    Map 3 - Niveau complexe

    Returns:
        tuple: (map_1,tour,tour_spawn_fantome)
    """
    map_3 = [
        list("CCCCCCCCCCCCCCCCCCCCC"),
        list("C E                 C"),
        list("C C C C C C C C C C C"),
        list("C MMMMMMMMMMMMMMMMM C"),
        list("C CMCMCMCMCMCMCMCMC C"),
        list("C MMMMMMMMMMMMMMMMM C"),
        list("C CMCMCMCMCMCMCMCMC C"),
        list("C MMMMMMMMMMMMMMMMM C"),
        list("C CMCMCMCMCMCMCMCMC C"),
        list("C MMMMMMMMMMMMMMMMM C"),
        list("C CMCMCMCMCMCMCMCMC C"),
        list("C        P          C"),
        list("C CMCMCMCMCMCMCMCMC C"),
        list("C MMMMMMMMMMMMMMMMM C"),
        list("C CMCMCMCMCMCMCMCMC C"),
        list("C MMMMMMMMMMMMMMMMM C"),
        list("C CMCMCMCMCMCMCMCMC C"),
        list("C MMMMMMMMMMMMMMMMM C"),
        list("C CMCMCMCMCMCMCMCMC C"),
        list("C                 E C"),
        list("CCCCCCCCCCCCCCCCCCCCC")
    ]
    tour = 1000
    tour_spawn_fantome = 20
    return map_3, tour, tour_spawn_fantome

def all_maps():
    """Retourne un dictionnaire des maps avec leur titre et fonction associée."""
    return {
        'map_1': {'title': 'Niveau Facile', 'function': map1},
        'map_2': {'title': 'Niveau Moyen', 'function': map2},
        'map_3': {'title': 'Niveau Difficile', 'function': map3},
    }

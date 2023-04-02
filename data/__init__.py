from .regions import forest, desert
from .equipment import boots, leggings, chestplates, helmets, weapons


# Top level interface to access various game data
game_data = {
    'regions': {
        'forest': forest.forest_region,
        'desert': desert.desert_region,
    },
    'equipment': {
        'boots': boots.boots,
        'leggings': leggings.leggings,
        'chestplates': chestplates.chestplates,
        'helmets': helmets.helmets,
        'weapons': weapons.weapons,
    },
}

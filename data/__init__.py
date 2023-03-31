from .regions import forest, desert
from classes.character import Enemy
from classes.stats import Stats
from classes.types import RaceType, EnemyType
from config import MINI_BOSS_SPAWN_CHANCE
import random


# Top level interface to access various game data
game_data = {
    'regions': {
        'forest': forest.forest_region,
        'desert': desert.desert_region,
    }
}


def get_random_enemy(region: str, player_level: int):
    '''Gets a random enemy from a specified region'''

    region = game_data['regions'][region]
    mini_boss_level_requirement = region['mini_boss_level_requirement']
    enemies = region['enemies']

    # Check if player is eligible for mini-bosses
    if player_level >= mini_boss_level_requirement and random.random() < MINI_BOSS_SPAWN_CHANCE:
        enemy = random.choice(enemies['mini_boss'])
        enemy_type = EnemyType.MINI_BOSS
    else:
        enemy = random.choice(enemies['normal'])
        enemy_type = EnemyType.NORMAL

    stats = {**enemy['stats'], 'hp': enemy['stats']['max_hp']}

    # Create Enemy instance
    return Enemy(
        name=enemy['name'],
        description=enemy['description'],
        race=RaceType(enemy['race']),
        enemy_type=enemy_type,
        loot_table=enemy['loot_table'],
        stats=Stats(**stats),
    )

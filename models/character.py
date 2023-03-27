from .stats import Stats
from .equipment import EquipmentInventory
from enum import Enum
import random
import json


class Race(Enum):
    HUMAN = 'human'
    ANIMAL = 'animal'
    PLANT = 'plant'
    BEAST = 'beast'
    UNDEAD = 'undead'
    ELEMENTAL = 'elemental'
    MONSTER = 'monster'


class EnemyType(Enum):
    NORMAL = 'normal'
    MINI_BOSS = 'mini_boss'
    BOSS = 'boss'


class Character:
    '''Base class for players and enemies'''

    def __init__(
        self,
        name: str,
        race: Race,
        stats: Stats,
        level: int,
    ):
        self.name = name
        self.race = race
        self.level = level
        self.stats = stats


class Player(Character):
    '''The main player of the game'''

    def __init__(
        self,
        name: str,
        race: Race,
        stats: Stats,
        equipment: EquipmentInventory,
        level: int = 1,
        inventory: list = [],
    ):
        super().__init__(name, race, stats, level)
        self.inventory = inventory
        self.equipment = equipment


class Enemy(Character):
    '''Enemies throughout the game'''

    def __init__(
        self,
        name: str,
        race: Race,
        stats: Stats,
        enemy_type: EnemyType,
        level: int = 1,
        loot_table: list = [],
    ):
        super().__init__(name, race, stats, level)
        self.enemy_type = enemy_type
        self.loot_table = loot_table


def get_random_enemy(region: str, player_level: int):
    with open("data/enemy.json", "r", encoding='utf-8') as file:
        _region = json.load(file)[region]

    enemies = _region['enemies']
    min_level_requirement = _region['min_level_requirement']
    mini_boss_level_requirement = _region['mini_boss_level_requirement']
    mini_boss_rarity = _region['mini_boss_rarity']
    enemy_list = []
    is_mini_boss = False

    # Check if player is allowed to fight in that area
    if player_level >= min_level_requirement:
        # Chance for mini-boss to spawn
        if player_level >= mini_boss_level_requirement and random.random() < mini_boss_rarity:
            enemy_list = [
                enemy for enemy in enemies['mini_boss'] if enemy['level'] <= player_level
            ]
            is_mini_boss = True
        # Fetch normal enemies instead
        if not enemy_list:
            enemy_list = [enemy for enemy in enemies['normal'] if enemy['level'] <= player_level]

        # Return a random enemy if there are any
        if enemy_list:
            enemy = random.choice(enemy_list)
            stats = enemy['stats']
            ret = Enemy(
                name=enemy['name'],
                race=enemy['race'],
                stats=Stats(
                    hp=stats['max_hp'],
                    attack=stats['attack'],
                    defense=stats['defense'],
                    cc=stats['cc'],
                    cd=stats['cd'],
                    max_hp=stats['max_hp'],
                ),
                enemy_type=EnemyType.MINI_BOSS if is_mini_boss else EnemyType.NORMAL,
                level=enemy['level'],
                loot_table=enemy['loot_table'],
            )
            file.close()
            return ret

        file.close()

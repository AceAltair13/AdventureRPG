from .entity import Entity
from .stats import Stats
from .equipment import EquipmentInventory
from .types import RaceType, EnemyType, ItemType
from .item import Item
import operator
import random
import json


class Character(Entity):
    '''Base class for players and enemies'''

    def __init__(
        self,
        name: str,
        description: str,
        race: RaceType,
        stats: Stats,
        level: int,
    ):
        super().__init__(name=name, description=description)
        self.race = race
        self.level = level
        self.stats = stats

    def take_damage(self, damage: int):
        final_hp = self.stats.hp - damage
        if final_hp < 0:
            self.stats.hp = 0
        else:
            self.stats.hp = final_hp

    def heal(self, heal: int):
        final_hp = self.stats.hp + heal
        if final_hp > self.stats.max_hp:
            self.stats.hp = self.stats.max_hp
        else:
            self.stats.hp = final_hp

    def is_alive(self):
        return self.stats.hp > 0


class Player(Character):
    '''The main player of the game'''

    def __init__(
        self,
        name: str,
        description: str,
        race: RaceType,
        stats: Stats,
        equipment: EquipmentInventory,
        level: int = 1,
        inventory: list[Item] = [],
    ):
        super().__init__(name, description, race, stats, level)
        self.actual_stats = stats
        self.inventory = inventory
        self.equipment = equipment
        self.effect_duration_remaining = 0  # Limits potion duration during battle

    def use_item(self, item: Item):
        # Check if item is potion
        if item.type == ItemType.CONSUMABLE:
            self.use_consumable(item)

        self.inventory.remove(item)

    def use_consumable(self, item: Item):
        # Modify the player stats according to effects list
        for effect in item.effects:
            stat, op, value = effect
            func = getattr(operator, op)
            final_value = func(getattr(self.stats, stat), value)
            if stat not in ('cc', 'cd'):
                final_value = round(final_value)
            setattr(self.stats, stat, final_value)

        # Check if the potion effect is permanent
        if item.duration == 0:
            self.actual_stats = self.stats
        else:
            self.effect_duration_remaining = item.duration

    def reset_effects(self):
        self.stats = self.actual_stats


class Enemy(Character):
    '''Enemies throughout the game'''

    def __init__(
        self,
        name: str,
        description: str,
        race: RaceType,
        stats: Stats,
        enemy_type: EnemyType,
        level: int = 1,
        loot_table: list = [],
    ):
        super().__init__(name, description, race, stats, level)
        self.enemy_type = enemy_type
        self.loot_table = loot_table

    # Get random enemy from a region. Can be normal or mini-boss
    @staticmethod
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
                enemy_list = [
                    enemy for enemy in enemies['normal'] if enemy['level'] <= player_level
                ]

            # Return a random enemy if there are any
            if enemy_list:
                enemy = random.choice(enemy_list)
                stats = enemy['stats']
                ret = Enemy(
                    name=enemy['name'],
                    description='',
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

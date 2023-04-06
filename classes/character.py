import operator
import random

from .enums import EnemyType, ItemType
from .entity import Entity
from .item import Item
from .stats import Stats
from .inventory import Inventory
from .equipment import Armor, Weapon
from config import MINI_BOSS_SPAWN_CHANCE


class Character(Entity):
    '''Base class for players and enemies'''

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        stats: Stats,
    ):
        super().__init__(id, name, description)
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
        id: str,
        name: str,
        description: str,
        stats: Stats = Stats(),
        inventory: Inventory = Inventory(),
        level: int = 1,
    ):
        super().__init__(id, name, description, stats)
        self.level = level
        self.inventory = inventory

    def use_item(self, item: Item):
        # Check if item is potion
        if item.item_type == ItemType.CONSUMABLE:
            self.use_consumable(item)

        self.inventory.bag.remove(item)

    def use_consumable(self, item: Item):
        # Modify the player stats according to effects list
        for effect in item.effects:
            stat, op, value, permanent = effect
            func = getattr(operator, op)
            final_value = func(getattr(self.stats, stat), value)
            if stat not in ('cc', 'cd'):
                final_value = round(final_value)
            setattr(self.stats, stat, final_value)
            if permanent:
                self.actual_stats = self.stats

    def reset_effects(self):
        self.stats = self.actual_stats

    def to_document(self):
        stats = self.stats.__dict__
        inventory = {
            'helmet': {
                'id': self.inventory.helmet.id,
                'level': self.inventory.helmet.current_level,
            },
            'chestplate': {
                'id': self.inventory.chestplate.id,
                'level': self.inventory.chestplate.current_level,
            },
            'leggings': {
                'id': self.inventory.leggings.id,
                'level': self.inventory.leggings.current_level,
            },
            'boots': {
                'id': self.inventory.boots.id,
                'level': self.inventory.boots.current_level,
            },
            'weapon': {
                'id': self.inventory.weapon.id,
                'level': self.inventory.weapon.current_level,
            },
            'accessory': {
                'id': self.inventory.accessory.id,
            },
            'bag': [item.id for item in self.inventory.bag],
        }

        return {
            '_id': self.id,
            'name': self.name,
            'description': self.description,
            'stats': stats,
            'inventory': inventory,
            'level': self.level,
        }

    @staticmethod
    def from_document(player: dict, game_data: dict):
        stats = Stats(**player['stats'])
        _inventory = player['inventory']
        inventory = Inventory(
            helmet=Armor(**game_data['items'][_inventory['helmet']['id']]),
            chestplate=Armor(**game_data['items'][_inventory['chestplate']['id']]),
            leggings=Armor(**game_data['items'][_inventory['leggings']['id']]),
            boots=Armor(**game_data['items'][_inventory['boots']['id']]),
            weapon=Weapon(**game_data['items'][_inventory['weapon']['id']]),
            accessory=Item(**game_data['items'][_inventory['accessory']['id']]),
            bag=[Item(**game_data['items'][item_id]) for item_id in _inventory['bag']],
        )

        return Player(
            id=player['_id'],
            name=player['name'],
            description=player['description'],
            stats=stats,
            inventory=inventory,
            level=player['level'],
        )


class Enemy(Character):
    '''Enemies throughout the game'''

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        stats: Stats,
        enemy_type: EnemyType,
        loot_table: list[tuple] = [],  # [(item_id, item_name, item_quantity)]
    ):
        super().__init__(id, name, description, stats)
        self.enemy_type = enemy_type
        self.loot_table = loot_table

    @staticmethod
    def get_random_enemy(game_data: dict, region: str, player_level: int):
        '''Gets a random enemy from a specified region'''

        _region = game_data['regions'][region]
        _enemies = _region['enemies']
        _mini_boss_level_requirement = _region['mini_boss_level_requirement']

        # Check if mini-boss can spawn
        if (
            player_level >= _mini_boss_level_requirement
            and MINI_BOSS_SPAWN_CHANCE > random.random()
        ):
            enemy = random.choice(_enemies['mini_boss'])
        else:
            enemy = random.choice(_enemies['regular'])

        _enemy_id = enemy['id']
        _enemy = game_data['enemies'][_enemy_id]
        _loot_table = enemy['loot_table']
        _loot = []

        for loot in _loot_table:
            if random.random() > loot['chance']:
                quantity = random.randint(loot['quantity'][0], loot['quantity'][1])
                name = game_data['items'][loot['id']]['name']
                item_id = loot['id']
                _loot.append((item_id, name, quantity))

        return Enemy(
            id=_enemy_id,
            name=_enemy['name'],
            description=_enemy['description'],
            stats=Stats(**_enemy['stats'], max_hp=_enemy['stats']['hp']),
            enemy_type=_enemy['enemy_type'],
            loot_table=_loot,
        )

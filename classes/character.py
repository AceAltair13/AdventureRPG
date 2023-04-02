import operator
import random

from data import game_data
from data.types import ArmorType, EnemyType, ItemType, RaceType
from .entity import Entity
from .equipment import Armor, EquipmentInventory, Weapon
from .item import Item
from .stats import Stats
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
        name: str,
        description: str,
        stats: Stats,
        equipment: EquipmentInventory = {},
        energy: int = 10,
        level: int = 1,
        inventory: list[Item] = [],
    ):
        super().__init__('player', name, description, stats)
        self.actual_stats = stats
        self.inventory = inventory
        self.equipment = equipment
        self.level = level
        self.energy = energy

    def use_item(self, item: Item):
        # Check if item is potion
        if item.type == ItemType.CONSUMABLE:
            self.use_consumable(item)

        self.inventory.remove(item)

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
        stats = {
            'hp': self.stats.hp,
            'max_hp': self.stats.max_hp,
            'cc': self.stats.cc,
            'cd': self.stats.cd,
            'attack': self.stats.attack,
            'defense': self.stats.defense,
        }
        inventory = [{'id': item.id, 'count': item.count} for item in self.inventory]
        equipment = {
            'helmet': {
                'id': self.equipment.helmet.id,
                'level': self.equipment.helmet.current_level,
            },
            'chestplate': {
                'id': self.equipment.chestplate.id,
                'level': self.equipment.chestplate.current_level,
            },
            'leggings': {
                'id': self.equipment.leggings.id,
                'level': self.equipment.leggings.current_level,
            },
            'boots': {
                'id': self.equipment.boots.id,
                'level': self.equipment.boots.current_level,
            },
            'weapon': {
                'id': self.equipment.weapon.id,
                'level': self.equipment.weapon.current_level,
            },
        }

        return {
            'name': self.name,
            'description': self.description,
            'stats': stats,
            'inventory': inventory,
            'equipment': equipment,
            'level': self.level,
            'energy': self.energy,
        }

    @staticmethod
    def from_document(_player: dict):
        stats = _player['stats']

        equipment = _player['equipment']

        equipment_inventory = EquipmentInventory(
            helmet=Armor(
                id=equipment['helmet']['id'],
                armor_type=ArmorType.HELMET,
                current_level=equipment['helmet']['level'],
                **game_data['equipment']['helmets'][equipment['helmet']['id']],
            ),
            chestplate=Armor(
                id=equipment['chestplate']['id'],
                armor_type=ArmorType.CHESTPLATE,
                current_level=equipment['chestplate']['level'],
                **game_data['equipment']['chestplates'][equipment['chestplate']['id']],
            ),
            leggings=Armor(
                id=equipment['leggings']['id'],
                armor_type=ArmorType.LEGGINGS,
                current_level=equipment['leggings']['level'],
                **game_data['equipment']['leggings'][equipment['leggings']['id']],
            ),
            boots=Armor(
                id=equipment['boots']['id'],
                armor_type=ArmorType.BOOTS,
                current_level=equipment['boots']['level'],
                **game_data['equipment']['boots'][equipment['boots']['id']],
            ),
            weapon=Weapon(
                id=equipment['weapon']['id'],
                current_level=equipment['weapon']['level'],
                **game_data['equipment']['weapons'][equipment['weapon']['id']],
            ),
        )

        _player['stats'] = Stats(**stats)
        _player['equipment'] = equipment_inventory

        return Player(**_player)


class Enemy(Character):
    '''Enemies throughout the game'''

    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        race: RaceType,
        stats: Stats,
        enemy_type: EnemyType,
        loot_table: dict,
    ):
        super().__init__(id, name, description, stats)
        self.race = race
        self.enemy_type = enemy_type
        self.loot_table = loot_table

    def generate_loot(self, luck: float):
        drops = []
        for item in self.loot_table:
            chance = item['chance']
            if chance <= 0.25:
                rarity = 'n `EPIC`'
            elif chance <= 0.5:
                rarity = ' `RARE`'
            elif chance <= 0.75:
                rarity = 'n `UNCOMMON`'
            else:
                rarity = ' `COMMON`'
            if random.random() < chance + luck:
                a, b = item['quantity']
                drops.append(
                    (
                        random.randint(a, b),
                        Item(
                            id=item['id'],
                            name=item['name'],
                            description=f'A{rarity} drop from the {self.name}',
                            item_type=ItemType.MATERIAL,
                            value=item['value'],
                        ),
                    )
                )
        return drops

    @staticmethod
    def get_random_enemy(region: str, player_level: int):
        '''Gets a random enemy from a specified region'''

        region = game_data['regions'][region]
        mini_boss_level_requirement = region['mini_boss_level_requirement']
        enemies = region['enemies']

        # Check if player is eligible for mini-bosses
        if (
            player_level >= mini_boss_level_requirement
            and random.random() < MINI_BOSS_SPAWN_CHANCE
        ):
            enemy = random.choice(enemies['mini_boss'])
            enemy_type = EnemyType.MINI_BOSS
        else:
            enemy = random.choice(enemies['normal'])
            enemy_type = EnemyType.NORMAL

        stats = {**enemy['stats'], 'hp': enemy['stats']['max_hp']}

        # Create Enemy instance
        return Enemy(
            id=enemy['id'],
            name=enemy['name'],
            description=enemy['description'],
            race=RaceType(enemy['race']),
            enemy_type=enemy_type,
            stats=Stats(**stats),
            loot_table=enemy['loot_table'],
        )

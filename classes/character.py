from .entity import Entity
from .stats import Stats
from .equipment import EquipmentInventory
from .types import RaceType, EnemyType, ItemType
from .item import Item
import operator


class Character(Entity):
    '''Base class for players and enemies'''

    def __init__(
        self,
        name: str,
        description: str,
        race: RaceType,
        stats: Stats,
    ):
        super().__init__(name=name, description=description)
        self.race = race
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
        energy: int = 10,
        level: int = 1,
        inventory: list[Item] = [],
    ):
        super().__init__(name, description, race, stats)
        self.actual_stats = stats
        self.inventory = inventory
        self.equipment = equipment
        self.level = level
        self.effect_duration_remaining = 0  # Limits potion duration during battle
        self.energy = energy

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
        loot_table: list = [],
    ):
        super().__init__(name, description, race, stats)
        self.enemy_type = enemy_type
        self.loot_table = loot_table

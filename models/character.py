from .stats import Stats
from .equipment import EquipmentInventory
from enum import Enum


class Race(Enum):
    HUMAN = 0
    ANIMAL = 1
    UNDEAD = 2
    ELEMENTAL = 3
    MONSTER = 4


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
        level: int = 1,
        loot_table: list = [],
    ):
        super().__init__(name, race, stats, level)
        self.loot_table = loot_table

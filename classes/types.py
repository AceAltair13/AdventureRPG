from enum import Enum


# Item categories
class ItemType(Enum):
    WEAPON = 1
    ARMOR = 2
    ACCESSORY = 3
    CONSUMABLE = 4
    MATERIAL = 5


# RaceType / Category types for characters
class RaceType(Enum):
    HUMAN = 'human'
    ANIMAL = 'animal'
    PLANT = 'plant'
    BEAST = 'beast'
    UNDEAD = 'undead'
    ELEMENTAL = 'elemental'
    MONSTER = 'monster'


# Enemy types
class EnemyType(Enum):
    NORMAL = 0
    MINI_BOSS = 1
    BOSS = 2


# Armor categories
class ArmorType(Enum):
    HELMET = 0
    CHESTPLATE = 1
    LEGGINGS = 2
    BOOTS = 3


# Weapon damage types
class WeaponType(Enum):
    PIERCING = 0
    SLASHING = 1
    BLUDGEONING = 2
    ICE = 3
    FIRE = 4
    ELECTRIC = 5
    POISON = 6
    RADIANT = 7

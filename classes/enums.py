from enum import Enum


# Item categories
class ItemType(Enum):
    ARMOR = 'armor'
    WEAPON = 'weapon'
    ACCESSORY = 'accessory'
    CONSUMABLE = 'consumable'
    MATERIAL = 'material'
    RESOURCE = 'resource'


# Armor categories
class ArmorType(Enum):
    HELMET = 'helmet'
    CHESTPLATE = 'chestplate'
    LEGGINGS = 'leggings'
    BOOTS = 'boots'


# Weapon damage types
class WeaponType(Enum):
    PIERCING = 'piercing'
    SLASHING = 'slashing'
    BLUDGEONING = 'bludgeoning'
    ICE = 'ice'
    FIRE = 'fire'
    ELECTRIC = 'electric'
    POISON = 'poison'
    RADIANT = 'radiant'


# Enemy types
class EnemyType(Enum):
    REGULAR = 'regular'
    MINI_BOSS = 'mini_boss'
    BOSS = 'boss'

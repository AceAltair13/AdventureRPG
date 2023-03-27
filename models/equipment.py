from enum import Enum


class ArmorType(Enum):
    HELMET = 0
    CHESTPLATE = 1
    LEGGINGS = 2
    BOOTS = 3


class WeaponType(Enum):
    PIERCING = 0
    SLASHING = 1
    BLUDGEONING = 2
    ICE = 3
    FIRE = 4
    ELECTRIC = 5
    POISON = 6
    RADIANT = 7


class Equipment:
    '''Base class for all equipments'''

    def __init__(self, name: str, required_level: int, current_level: int = 1):
        self.name = name
        self.required_level = required_level
        self.current_level = current_level


class Armor(Equipment):
    '''Model class for armors'''

    def __init__(
        self,
        name: str,
        required_level: int,
        armor_type: ArmorType,
        defense: int,
    ):
        super().__init__(name, required_level)
        self.armor_type = armor_type
        self.defense = defense


class Weapon(Equipment):
    '''Model class for weapons'''

    def __init__(
        self,
        name: str,
        required_level: int,
        weapon_type: WeaponType,
        attack: int,
    ):
        super().__init__(name, required_level)
        self.weapon_type = weapon_type
        self.attack = attack


class EquipmentInventory:
    '''Equipment containing armor and weapon'''

    def __init__(
        self,
        helmet: Armor,
        chestplate: Armor,
        leggings: Armor,
        boots: Armor,
        weapon: Weapon,
    ):
        self.helmet = helmet
        self.chestplate = chestplate
        self.leggings = leggings
        self.boots = boots
        self.weapon = weapon

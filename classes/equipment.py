from .item import Item
from .types import ArmorType, WeaponType, ItemType


class Equipment(Item):
    '''Base class for all equipments'''

    def __init__(
        self,
        name: str,
        description: str,
        item_type: ItemType,
        required_level: int,
        current_level: int = 1,
    ):
        super().__init__(name=name, description=description, item_type=item_type)
        self.required_level = required_level
        self.current_level = current_level


class Armor(Equipment):
    '''Model class for armors'''

    def __init__(
        self,
        name: str,
        description: str,
        required_level: int,
        armor_type: ArmorType,
        defense: int,
    ):
        super().__init__(
            name=name,
            description=description,
            item_type=ItemType.ARMOR,
            required_level=required_level,
        )
        self.armor_type = armor_type
        self.defense = defense


class Weapon(Equipment):
    '''Model class for weapons'''

    def __init__(
        self,
        name: str,
        description: str,
        required_level: int,
        weapon_type: WeaponType,
        attack: int,
    ):
        super().__init__(
            name=name,
            description=description,
            item_type=ItemType.WEAPON,
            required_level=required_level,
        )
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

from data.equipment.armor.helmet import helmets
from data.equipment.armor.chestplate import chestplates
from data.equipment.armor.leggings import leggings
from data.equipment.armor.boots import boots
from data.equipment.weapon import weapons
from data.equipment.accessory import accessories
from .equipment import Armor, Weapon
from .item import Item
from .enums import ArmorType, ItemType


class Inventory:
    '''Inventory of the player'''

    # Defaults
    default_helmet = Armor(
        **helmets[0],
        armor_type=ArmorType.HELMET,
        item_type=ItemType.ARMOR,
    )
    default_chestplate = Armor(
        **chestplates[0],
        armor_type=ArmorType.CHESTPLATE,
        item_type=ItemType.ARMOR,
    )
    default_leggings = Armor(
        **leggings[0],
        armor_type=ArmorType.LEGGINGS,
        item_type=ItemType.ARMOR,
    )
    default_boots = Armor(
        **boots[0],
        armor_type=ArmorType.BOOTS,
        item_type=ItemType.ARMOR,
    )
    default_weapon = Weapon(**weapons[0], item_type=ItemType.WEAPON)
    default_accessory = Item(**accessories[0], item_type=ItemType.ACCESSORY)

    def __init__(
        self,
        helmet: Armor = default_helmet,
        chestplate: Armor = default_chestplate,
        leggings: Armor = default_leggings,
        boots: Armor = default_boots,
        weapon: Weapon = default_weapon,
        accessory: Item = default_accessory,
        bag: list[Item] = [],
    ):
        self.helmet = helmet
        self.chestplate = chestplate
        self.leggings = leggings
        self.boots = boots
        self.weapon = weapon
        self.accessory = accessory
        self.bag = bag

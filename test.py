from classes.character import Player, RaceType
from classes.equipment import Armor, ArmorType, Weapon, WeaponType, EquipmentInventory
from classes.item import Item
from classes.stats import Stats
from classes.types import ItemType


# Sample player
player = Player(
    name='You',
    race=RaceType.HUMAN,
    description='',
    stats=Stats(100, 5, 0, 0.0, 1.5, 100),
    equipment=EquipmentInventory(
        helmet=Armor('No Helmet', '', 0, ArmorType.HELMET, 0),
        chestplate=Armor('No Helmet', '', 0, ArmorType.CHESTPLATE, 0),
        leggings=Armor('No Helmet', '', 0, ArmorType.LEGGINGS, 0),
        boots=Armor('No Helmet', '', 0, ArmorType.BOOTS, 0),
        weapon=Weapon('Fist', '', 0, WeaponType.BLUDGEONING, 1),
    ),
    inventory=[
        Item(
            name='🧪❤️ Potion of Healing',
            description='[ +10 HP ]',
            item_type=ItemType.CONSUMABLE,
            effects=[('hp', 'add', 10)],
        )
    ],
    level=1,
)

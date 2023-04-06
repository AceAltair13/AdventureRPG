from classes.enums import ArmorType, EnemyType, ItemType

# Enemies
from .enemies.boss import boss
from .enemies.miniboss import mini_boss
from .enemies.regular import regular

# Items
from .equipment.accessory import accessories
from .equipment.weapon import weapons
from .equipment.armor.helmet import helmets
from .equipment.armor.chestplate import chestplates
from .equipment.armor.leggings import leggings
from .equipment.armor.boots import boots
from .items.resource import resources
from .items.material import materials
from .items.consumable import consumables

# Regions
from .regions.forest import forest
from .regions.desert import desert


def load_data() -> dict:
    '''Load the game data'''

    game_data = {}

    # Load enemies
    enemies = {}
    _enemies = [
        (regular, EnemyType.REGULAR),
        (mini_boss, EnemyType.MINI_BOSS),
        (boss, EnemyType.BOSS),
    ]
    for enemy_list, enemy_type in _enemies:
        for enemy in enemy_list:
            enemy['enemy_type'] = enemy_type
            enemies[enemy['id']] = enemy
    game_data['enemies'] = enemies

    # Load items
    items = {}
    _items = [
        (weapons, ItemType.WEAPON),
        (accessories, ItemType.ACCESSORY),
        (materials, ItemType.MATERIAL),
        (consumables, ItemType.CONSUMABLE),
        (resources, ItemType.RESOURCE),
    ]
    for item_list, item_type in _items:
        for item in item_list:
            item['item_type'] = item_type
            items[item['id']] = item
    _armor = [
        (helmets, ArmorType.HELMET),
        (chestplates, ArmorType.CHESTPLATE),
        (leggings, ArmorType.LEGGINGS),
        (boots, ArmorType.BOOTS),
    ]
    for armor_list, armor_type in _armor:
        for armor in armor_list:
            armor['item_type'] = ItemType.ARMOR
            armor['armor_type'] = armor_type
            items[armor['id']] = armor
    game_data['items'] = items

    # Load regions
    regions = {}
    _regions = [forest, desert]
    for region in _regions:
        regions[region['id']] = region
    game_data['regions'] = regions

    print("Game data loaded successfully!")

    return game_data

from pymongo import MongoClient, ReturnDocument
from config import MONGODB_URI
from classes.types import ArmorType, WeaponType
from classes.character import Player
from classes.stats import Stats
from classes.equipment import EquipmentInventory, Armor, Weapon
from data import game_data
import errors


# Get the client
client = MongoClient(MONGODB_URI)

# Create a db instance
db = client.adventureRPG

# Get the player collection
players = db.players


def player_exists(id: int):
    '''Check if the player exists in the db'''
    return players.count_documents({'_id': str(id)}) != 0


def create_player(id: int, name: str, description: str):
    '''Create a new player in the players collection'''
    player = {
        '_id': str(id),
        'name': name,
        'description': description,
        'level': 1,
        'inventory': [],
        'stats': {'hp': 100, 'attack': 5, 'defense': 0, 'cc': 0.0, 'cd': 1.5, 'max_hp': 100},
        'equipment': {
            'weapon': {
                'item_id': 'no_weapon',
                'level': 1,
            },
            'helmet': {
                'item_id': 'no_helmet',
                'level': 1,
            },
            'chestplate': {
                'item_id': 'no_chestplate',
                'level': 1,
            },
            'leggings': {
                'item_id': 'no_leggings',
                'level': 1,
            },
            'boots': {
                'item_id': 'no_boots',
                'level': 1,
            },
        },
        'energy': 10,
    }
    id = players.insert_one(player).inserted_id
    if id is None:
        raise errors.DatabaseSaveError


def get_player(id: int, energy_consumed: int = 0) -> Player:
    '''Get the player from the players collection'''

    if not player_exists(str(id)):
        raise errors.PlayerNotCreated

    filter = {'_id': str(id)}
    if energy_consumed > 0:
        filter['energy'] = {'$gte': energy_consumed}

    projection = {'_id': 0}
    update = {'$inc': {'energy': -energy_consumed}} if energy_consumed else None
    _player = players.find_one_and_update(
        filter=filter, projection=projection, update=update, return_document=ReturnDocument.AFTER
    )

    if energy_consumed and _player is None:
        raise errors.PlayerHasNoEnergy

    stats = _player['stats']
    equipment = _player['equipment']

    equipment_inventory = EquipmentInventory(
        helmet=Armor(
            item_id=equipment['helmet']['item_id'],
            armor_type=ArmorType.HELMET,
            current_level=equipment['helmet']['level'],
            **game_data['equipment']['helmets'][equipment['helmet']['item_id']]
        ),
        chestplate=Armor(
            item_id=equipment['chestplate']['item_id'],
            armor_type=ArmorType.CHESTPLATE,
            current_level=equipment['chestplate']['level'],
            **game_data['equipment']['chestplates'][equipment['chestplate']['item_id']]
        ),
        leggings=Armor(
            item_id=equipment['leggings']['item_id'],
            armor_type=ArmorType.LEGGINGS,
            current_level=equipment['leggings']['level'],
            **game_data['equipment']['leggings'][equipment['leggings']['item_id']]
        ),
        boots=Armor(
            item_id=equipment['boots']['item_id'],
            armor_type=ArmorType.BOOTS,
            current_level=equipment['boots']['level'],
            **game_data['equipment']['boots'][equipment['boots']['item_id']]
        ),
        weapon=Weapon(
            item_id=equipment['weapon']['item_id'],
            current_level=equipment['weapon']['level'],
            **game_data['equipment']['weapons'][equipment['weapon']['item_id']]
        ),
    )

    _player['stats'] = Stats(**stats)
    _player['equipment'] = equipment_inventory

    return Player(**_player)


def update_player(id: int, player: Player):
    '''Update a player in the players collection'''
    count = players.update_one({'_id': str(id)}, {'$set': player.document()}).modified_count
    if count == 0:
        raise errors.DatabaseSaveError


def update_player_field(id: int, field: str, value):
    '''Update a player field in the players collection'''
    count = players.update_one({'_id': str(id)}, {'$set': {field: value}}).modified_count
    if count == 0:
        raise errors.DatabaseSaveError


def consume_player_energy(id: int, amount: int = 1) -> int:
    '''Consume player energy and return the modified energy'''
    _player = players.find_one_and_update(
        filter={'_id': str(id)},
        projection={'energy': 1},
        update={'$inc': {'energy': -amount}},
        return_document=ReturnDocument.AFTER,
    )
    if _player is None:
        raise errors.PlayerNotFound
    return _player['energy']


def delete_player(id: int):
    '''Delete a player from the database'''
    count = players.delete_one({'_id': str(id)}).deleted_count
    if count == 0:
        raise errors.PlayerNotFound

import utils.errors as errors

from pymongo import MongoClient, ReturnDocument
from config import MONGODB_URI
from classes.character import Player

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
    _player = Player(str(id), name, description)
    _id = players.insert_one(_player.to_document()).inserted_id
    if _id is None:
        raise errors.DatabaseSaveError


def get_player(id: int, game_data: dict, energy_consumed: int = 0) -> Player:
    '''Get the player from the players collection'''

    if not player_exists(str(id)):
        raise errors.PlayerNotCreated

    filter = {'_id': str(id)}
    if energy_consumed > 0:
        filter['energy'] = {'$gte': energy_consumed}

    update = {'$inc': {'energy': -energy_consumed}} if energy_consumed else None
    _player = players.find_one_and_update(
        filter=filter, update=update, return_document=ReturnDocument.AFTER
    )

    if energy_consumed and _player is None:
        raise errors.PlayerHasNoEnergy

    return Player.from_document(_player, game_data)


def update_player(id: int, player: Player):
    '''Update a player in the players collection'''
    count = players.update_one({'_id': str(id)}, {'$set': player.to_document()}).modified_count
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

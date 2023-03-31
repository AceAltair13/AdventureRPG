from pymongo import MongoClient
from config import MONGODB_URI
from classes.character import Player
from classes.types import ArmorType, WeaponType
import bson

# Get the client
client = MongoClient(MONGODB_URI)

# Create a db instance
db = client.adventureRPG

# Get the player collection
players = db.players


# Check if the player exists in the db
def player_exists(id: int):
    id = str(id)
    return players.count_documents({'_id': id}) != 0


# Create a new player in the players collection
def create_player(id: int, name: str, description: str):
    # equipment = {
    #     'helmet': {
    #         'name': 'No Helmet',
    #         'description': '',
    #         'required_level': 1,
    #         'armor_type': ArmorType.HELMET.value,
    #         'defense': 0,
    #     },
    #     'chestplate': {
    #         'name': 'No Chestplate',
    #         'description': '',
    #         'required_level': 1,
    #         'armor_type': ArmorType.CHESTPLATE.value,
    #         'defense': 0,
    #     },
    #     'leggings': {
    #         'name': 'No Leggings',
    #         'description': '',
    #         'required_level': 1,
    #         'armor_type': ArmorType.LEGGINGS.value,
    #         'defense': 0,
    #     },
    #     'boots': {
    #         'name': 'No Boots',
    #         'description': '',
    #         'required_level': 1,
    #         'armor_type': ArmorType.BOOTS.value,
    #         'defense': 0,
    #     },
    #     'weapon': {
    #         'name': 'Fist',
    #         'description': '',
    #         'required_level': 1,
    #         'weapon_type': WeaponType.BLUDGEONING.value,
    #         'attack': 5,
    #     },
    # }

    # defense = (
    #     equipment['helmet']['defense']
    #     + equipment['chestplate']['defense']
    #     + equipment['leggings']['defense']
    #     + equipment['boots']['defense']
    # )

    # stats = {
    #     'hp': 100,
    #     'attack': equipment['weapon']['attack'],
    #     'defense': defense,
    #     'cc': 0.0,
    #     'cd': 1.5,
    #     'max_hp': 100,
    # }
    id = str(id)
    player = {
        '_id': id,
        'name': name,
        'description': description,
        'race': 'human',
        'level': 1,
        'inventory': [],
        'equipment': {'Helmet': 'no_helmet'},
    }

    return players.insert_one(player).acknowledged


# Get a player from the players collection
def get_player(id: int) -> Player:
    id = str(id)
    player = players.find_one({'_id': id})


def delete_player(id: int):
    id = str(id)
    return players.delete_one({'_id': id}).deleted_count > 0


# print(players.find_one({'_id': '345246015882002433'}))

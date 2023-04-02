class Entity:
    '''Base class for every in-game entity'''

    def __init__(self, id: str, name: str, description: str):
        self.id = id
        self.name = name
        self.description = description

class Entity:
    '''Base class for every in-game entity'''

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

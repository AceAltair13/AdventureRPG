class Stats:
    '''The stats of a character'''

    def __init__(
        self,
        hp: float,
        attack: int,
        defense: int,
        cc: float,
        cd: float,
        max_hp: float,
    ):
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.cc = cc
        self.cd = cd
        self.max_hp = max_hp

from discord import Embed, Color


class AdventureRPGException(Exception):
    '''Custom exception class for AdventureRPG'''

    def __init__(
        self,
        title: str,
        message: str = None,
    ):
        self.title = title
        self.message = message

    def get_embed(self):
        '''Return an error embed'''
        return Embed(
            title=self.title,
            description=self.message,
            color=Color.red(),
        )


class NotAnAdmin(AdventureRPGException):
    '''If the player is not an admin'''

    def __init__(self):
        super().__init__(title='You are not permitted to use that command')


class DatabaseSaveError(AdventureRPGException):
    '''If there was a problem performing CRUD on the DB'''

    def __init__(self):
        super().__init__(
            title='Error Saving Data',
            message='Your data could not be saved due to an error. Please try again.',
        )


class DatabaseDeleteError(AdventureRPGException):
    '''If there was a problem deleting data from the DB'''

    def __init__(self):
        super().__init__(
            title='Error Deleting Data',
            message='There was a problem deleting one or more data from the database. Please try again.',
        )


class PlayerNotCreated(AdventureRPGException):
    '''If the player hasn't been created yet in the database'''

    def __init__(self):
        super().__init__(
            title='Welcome to AdventureRPG!',
            message='Please create a character first using `/start` before you can start using this command.',
        )


class PlayerNotFound(AdventureRPGException):
    '''If the player doesn't exist in the database'''

    def __init__(self):
        super().__init__(
            title='Player Not Found',
            message='The player you have requested could not be located in the database. Please check your query.',
        )


class PlayerAlreadyExists(AdventureRPGException):
    '''If the player already exists in the database'''

    def __init__(self):
        super().__init__(
            title='Player Already Exists',
            message='This command is only available for players who haven\'t started playing yet.',
        )


class PlayerHasNoEnergy(AdventureRPGException):
    '''If the player has no energy'''

    def __init__(self):
        super().__init__(
            title='Out Of Energy',
            message='Sorry, you don\'t have enough energy to use this command. Please use `/rest` to start gaining energy.',
        )

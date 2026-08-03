from src.database.session import DatabaseSession


class BaseRepository:

    def __init__(self, session: DatabaseSession):

        self.session = session

        self.cursor = session.cursor
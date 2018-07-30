import collections

from .base import BaseCassandraDataProvider, BaseDataProvider


User = collections.namedtuple('User', ['username'])


class CassandraUserDataProvider(BaseCassandraDataProvider):

    def get(self, username):
        row = self._session.execute(
            'SELECT username FROM user WHERE username = %s', [username],
        ).one()

        if row is None:
            return None

        return self._build_from_row(row)

    def list(self):
        users = []
        for row in self._session.execute('SELECT username FROM user'):
            user = self._build_from_row(row)
            users.append(user)
        return users

    def create(self, username):
        self._session.execute('INSERT INTO user (username) VALUES (%s)', [username])
        return User(username=username)

    def _build_from_row(self, row):
        return User(username=row.username)


class StubUserDataProvider(BaseDataProvider):

    users = {}

    @classmethod
    def clear(cls):
        cls.users = {}

    def get(self, username):
        return self.users.get(username)

    def list(self):
        return list(self.users.values())

    def create(self, username):
        user = User(username=username)
        self.users[username] = user
        return user

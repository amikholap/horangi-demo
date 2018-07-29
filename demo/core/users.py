import cassandra.cluster

from .base import BaseDataProvider


class User:

    def __init__(self, username):
        self.username = username


class CassandraDataProvider(BaseDataProvider):

    def __init__(self, hosts, keyspace):
        self._cluster = cassandra.cluster.Cluster(hosts)
        self._session = self._cluster.connect()
        self._session.set_keyspace(keyspace)

    def get_users(self):
        users = []
        for (username,) in self._session.execute('SELECT username FROM user'):
            user = User(username)
            users.append(user)
        return users

    def create_user(self, username):
        self._session.execute('INSERT INTO user (username) VALUES (%s)', [username])
        return User(username=username)


class StubUsersDataProvider(BaseDataProvider):

    def __init__(self):
        self.users = {}

    def get_users(self):
        return list(self.users.values())

    def create_user(self, username):
        user = User(username=username)
        self.users[username] = user
        return user

from .base import BaseDataProvider


class User:

    def __init__(self, username):
        self.username = username


class StubUsersDataProvider(BaseDataProvider):

    @classmethod
    def from_settings(cls):
        return cls()

    def __init__(self):
        self.users = {}

    def get_users(self):
        return list(self.users.values())

    def create_user(self, username):
        user = User(username=username)
        self.users[username] = user
        return user

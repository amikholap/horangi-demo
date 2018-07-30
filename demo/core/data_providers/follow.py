import collections

from .base import BaseCassandraDataProvider, BaseDataProvider


Follow = collections.namedtuple('Follow', ['followee', 'follower', 'created_at'])


class CassandraFollowDataProvider(BaseCassandraDataProvider):
    pass


class StubFollowDataProvider(BaseDataProvider):

    follows = collections.defaultdict(set)

    @classmethod
    def clear(cls):
        cls.follows = collections.defaultdict(set)

    def create(self, followee, follower, created_at):
        follow = Follow(
            followee=followee,
            follower=follower,
            created_at=created_at,
        )
        self.follows[followee].add(follow)
        return follow

    def get_follow(self, followee, follower):
        for follow in self.follows[followee]:
            if follower == follower:
                return follow
        return None

    def get_followers(self, username):
        return self.follows(username)

    def delete(self, followee, follower):
        try:
            self.follows[followee].remove(follower)
        except KeyError:
            return False
        return True

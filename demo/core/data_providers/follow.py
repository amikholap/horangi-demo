import collections

from .base import BaseCassandraDataProvider, BaseDataProvider


Follow = collections.namedtuple('Follow', ['followee', 'follower', 'created_at'])


class CassandraFollowDataProvider(BaseCassandraDataProvider):

    def get(self, followee, follower):
        query = (
            'SELECT followee_username, follower_username, created_at '
            'FROM follow '
            'WHERE followee_username = %s AND follower_username = %s '
            'ALLOW FILTERING'
        )

        row = self._session.execute(query, [followee, follower]).one()
        if row is None:
            return None

        follow = self._build_from_row(row)

        return follow

    def get_followees(self, username):
        """
        Get all people that a username follows.

        Slow since the request touches every partition.
        The result should be cached.
        """

        query = (
            'SELECT followee_username '
            'FROM follow '
            'WHERE follower_username = %s '
            'ALLOW FILTERING'
        )

        results = self._session.execute(query, [username])
        followees = [row.followee_username for row in results]

        return followees

    def create(self, followee, follower, created_at):
        query = (
            'INSERT INTO follow '
            '(followee_username, follower_username, created_at) '
            'VALUES (%s, %s, %s)'
        )
        self._session.execute(query, [followee, follower, created_at])
        return Follow(
            followee=followee,
            follower=follower,
            created_at=created_at,
        )

    def delete(self, followee, follower):
        query = (
            'DELETE FROM follow '
            'WHERE followee_username = %s AND follower_username = %s '
            'IF EXISTS'
        )
        result = self._session.execute(query, [followee, follower])
        return result.one().applied

    def _build_from_row(self, row):
        return Follow(
            followee=row.followee_username,
            follower=row.follower_username,
            created_at=row.created_at,
        )


class StubFollowDataProvider(BaseDataProvider):

    follows = collections.defaultdict(set)

    @classmethod
    def clear(cls):
        cls.follows = collections.defaultdict(set)

    def get(self, followee, follower):
        for follow in self.follows[followee]:
            if followee == follower:
                return follow
        return None

    def get_followees(self, username):
        return {
            followee
            for followee, follows in self.follows.items()
            if username in {f.follower for f in follows}
        }

    def create(self, followee, follower, created_at):
        follow = Follow(
            followee=followee,
            follower=follower,
            created_at=created_at,
        )
        self.follows[followee].add(follow)
        return follow

    def delete(self, followee, follower):
        try:
            self.follows[followee].remove(follower)
        except KeyError:
            return False
        return True

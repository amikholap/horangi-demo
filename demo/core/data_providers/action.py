import collections

import cassandra.query

from .base import BaseCassandraDataProvider, BaseDataProvider


Action = collections.namedtuple(
    'Action',
    ['actor_username', 'created_at', 'id', 'verb', 'object', 'target_username'],
)


class CassandraActionDataProvider(BaseCassandraDataProvider):

    def create(self, actor_username, created_at, id_, verb, object_, target_username):
        query = (
            'INSERT INTO action '
            '(actor_username, created_at, id, verb, object, target_username) '
            'VALUES (%s, %s, %s, %s, %s, %s)'
        )
        self._session.execute(
            query,
            [actor_username, created_at, id_, verb, object_, target_username],
        )
        return Action(
            actor_username=actor_username,
            created_at=created_at,
            id=id_,
            verb=verb,
            object=object_,
            target_username=target_username,
        )

    def list(self, actor_username, page, page_size):
        # Linear time performance wrt the last element position
        # since Cassandra doesn't natively support OFFSET.

        offset = page * page_size
        limit = (page + 1) * page_size

        if isinstance(actor_username, str):
            results = self._list_single_actor(actor_username, limit)
        else:
            results = self._list_multiple_actors(actor_username, limit)

        actions = [self._build_from_row(row) for i, row in enumerate(results) if i >= offset]

        return actions

    def _list_single_actor(self, username, limit):
        query = (
            'SELECT actor_username, created_at, id, verb, object, target_username '
            'FROM action '
            'WHERE actor_username = %s '
            'LIMIT %s'
        )
        results = self._session.execute(query, [username, limit])
        return results

    def _list_multiple_actors(self, usernames, limit):
        # Slow and touches up to every partition.
        # The results should be cached.
        query = (
            'SELECT actor_username, created_at, id, verb, object, target_username '
            'FROM action '
            'WHERE actor_username IN %s '
            'LIMIT %s '
            'ALLOW FILTERING'
        )
        results = self._session.execute(query, [cassandra.query.ValueSequence(usernames), limit])
        return results

    def _build_from_row(self, row):
        return Action(
            actor_username=row.actor_username,
            created_at=row.created_at,
            id=row.id,
            verb=row.verb,
            object=row.object,
            target_username=row.target_username,
        )


class StubActionDataProvider(BaseDataProvider):

    actions = []

    @classmethod
    def clear(cls):
        cls.actions = []

    def create(self, actor_username, created_at, id_, verb, object_, target_username):
        action = Action(
            actor_username=actor_username,
            created_at=created_at,
            id=id_,
            verb=verb,
            object=object_,
            target_username=target_username,
        )

        if self.actions:
            assert action.created_at >= self.actions[-1].created_at

        self.actions.append(action)

        return action

    def list(self, actor_username, page, page_size):
        if isinstance(actor_username, str):
            actor_username = [actor_username]

        actions = []
        for action in self.actions:
            for username in actor_username:
                if action.actor_username == username:
                    actions.append(action)

        low, high = page * page_size, (page + 1) * page_size
        actions = actions[low:high]

        return actions

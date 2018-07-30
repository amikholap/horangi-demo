import collections

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

        query = (
            'SELECT actor_username, created_at, id, verb, object, target_username '
            'FROM action '
            'WHERE actor_username = %s '
            'LIMIT %s'
        )

        rows = self._session.execute(query, [actor_username, limit])
        actions = [self._build_from_row(row) for i, row in enumerate(rows) if i >= offset]

        return actions

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
        actions = [action for action in self.actions if action.actor_username == actor_username]
        low, high = page * page_size, (page + 1) * page_size
        actions = actions[low:high]
        return actions

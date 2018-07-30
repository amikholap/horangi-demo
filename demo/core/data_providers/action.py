import collections

from .base import BaseCassandraDataProvider, BaseDataProvider


Action = collections.namedtuple(
    'Action',
    ['actor_username', 'created_at', 'id', 'verb', 'object', 'target_username'],
)


class CassandraActionDataProvider(BaseCassandraDataProvider):
    pass


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

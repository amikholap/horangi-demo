import uuid

from django.conf import settings
from django.utils import timezone

from ..data_providers.base import BaseDataProvider
from .base import BaseController


class ActionController(BaseController):

    class Error(Exception):
        def __init__(self, code):
            super().__init__(code)
            self.code = code

    @classmethod
    def from_settings(cls):
        action_dp = BaseDataProvider.from_settings(settings.DATA_PROVIDERS['action'])
        user_dp = BaseDataProvider.from_settings(settings.DATA_PROVIDERS['user'])
        return cls(
            action_data_provider=action_dp,
            user_data_provider=user_dp,
        )

    def __init__(self, action_data_provider, user_data_provider):
        self.action_dp = action_data_provider
        self.user_dp = user_data_provider

    def create_action(self, actor, verb, object_, target):
        if self.user_dp.get(actor) is None:
            raise self.Error('actor.invalid')
        if target is not None and self.user_dp.get(target) is None:
            raise self.Error('target.invalid')

        created_at = timezone.now()
        action = self.action_dp.create(
            actor_username=actor,
            created_at=created_at,
            id_=uuid.uuid1(),
            verb=verb,
            object_=object_,
            target_username=target,
        )

        # At this point the action should be submitted to a persistent distibuted queue
        # for further async processing like updating caches and creating related action index.

        # Created the related action in synchronous manner instead.
        # This can fail and leave related action index inconsistent.
        self.create_related_action(
            object_=action.object,
            created_at=action.created_at,
            actor=action.actor_username,
            id_=action.id,
            verb=action.verb,
            target=action.target_username,
        )

        return action

    def create_related_action(self, object_, created_at, actor, id_, verb, target):
        related_action = self.action_dp.create_related(
            object_=object_,
            created_at=created_at,
            actor_username=actor,
            id_=id_,
            verb=verb,
            target_username=target,
        )
        return related_action

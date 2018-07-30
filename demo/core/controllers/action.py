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

        # At this point the action should be submitted
        # to a persistent distibuted queue for further async processing like updating caches.

        return action

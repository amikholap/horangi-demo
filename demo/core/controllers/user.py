import logging

from django.conf import settings
from django.utils import timezone

from ..data_providers.base import BaseDataProvider
from .action import ActionController
from .base import BaseController


LOGGER = logging.getLogger(__name__)


class UserController(BaseController):

    class Error(Exception):
        def __init__(self, code):
            super().__init__(code)
            self.code = code

    @classmethod
    def from_settings(cls):
        follow_dp = BaseDataProvider.from_settings(settings.DATA_PROVIDERS['follow'])
        user_dp = BaseDataProvider.from_settings(settings.DATA_PROVIDERS['user'])
        action_controller = ActionController.from_settings()
        return cls(
            follow_data_provider=follow_dp,
            user_data_provider=user_dp,
            action_controller=action_controller,
        )

    def __init__(self, follow_data_provider, user_data_provider, action_controller):
        self.follow_dp = follow_data_provider
        self.user_dp = user_data_provider
        self.action_controller = action_controller

    def create_user(self, username):
        return self.user_dp.create(username=username)

    def follow(self, followee, follower):
        if self.user_dp.get(followee) is None:
            raise self.Error('followee.invalid')
        if self.user_dp.get(follower) is None:
            raise self.Error('follower.invalid')

        created_at = timezone.now()
        follow = self.follow_dp.create(
            followee=followee,
            follower=follower,
            created_at=created_at,
        )

        # This should be done async by passing the event into a queue.
        self.action_controller.create_action(
            actor=follower,
            verb='follow',
            object_=None,
            target=followee,
            created_at=created_at,
        )

        return follow

    def unfollow(self, followee, follower):
        if self.user_dp.get(followee) is None:
            raise self.Error('followee.invalid')
        if self.user_dp.get(follower) is None:
            raise self.Error('follower.invalid')

        if not self.follow_dp.delete(followee, follower):
            # Don't raise an error to keep the operation idempotent.
            LOGGER.info('tried to delete nonexistent follow %s -> %s', followee, follower)

        self.action_controller.create_action(
            actor=follower,
            verb='unfollow',
            object_=None,
            target=followee,
        )

import logging

from django.conf import settings
from django.utils import timezone

from ..data_providers.base import BaseDataProvider
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
        return cls(
            follow_data_provider=follow_dp,
            user_data_provider=user_dp,
        )

    def __init__(self, follow_data_provider, user_data_provider):
        self.follow_dp = follow_data_provider
        self.user_dp = user_data_provider

    def create_user(self, username):
        return self.user_dp.create(username=username)

    def follow(self, followee, follower):
        if self.user_dp.get(followee) is None:
            raise self.Error('followee.invalid')
        if self.user_dp.get(follower) is None:
            raise self.Error('follower.invalid')

        created_at = timezone.now()
        return self.follow_dp.create(
            followee=followee,
            follower=follower,
            created_at=created_at,
        )

    def unfollow(self, followee, follower):
        if self.user_dp.get(followee) is None:
            raise self.Error('followee.invalid')
        if self.user_dp.get(follower) is None:
            raise self.Error('follower.invalid')
        if self.follow_dp.get_follow(followee, follower) is None:
            raise self.Error('not_followed')

        if not self.follow_dp.delete(follower, follower):
            # Don't raise an error to keep the operation idempotent.
            LOGGER.info('tried to delete nonexistent follow %s -> %s', followee, follower)

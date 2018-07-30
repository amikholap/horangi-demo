from .settings import *


DATA_PROVIDERS = {
    'follow': {
        'class': 'demo.core.data_providers.follow.StubFollowDataProvider',
        'params': {},
    },
    'user': {
        'class': 'demo.core.data_providers.user.StubUserDataProvider',
        'params': {},
    },
}

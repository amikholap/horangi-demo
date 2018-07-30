from rest_framework.serializers import CharField

from demo.drf.serializers import BaseSerializer


class FollowArgumentsSerializer(BaseSerializer):
    followee = CharField()
    follower = CharField()


class UserSerializer(BaseSerializer):
    username = CharField()

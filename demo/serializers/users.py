from rest_framework.serializers import CharField

from demo.drf.serializers import BaseSerializer


class UserSerializer(BaseSerializer):
    username = CharField()

from rest_framework.serializers import CharField, DateTimeField, IntegerField

from demo.drf.serializers import BaseSerializer


class ActionArgumentsSerializer(BaseSerializer):
    actor = CharField()
    verb = CharField()
    object = CharField()
    target = CharField(allow_null=True)


class ActionFeedArgumentsSerializer(BaseSerializer):
    actor = CharField()
    page = IntegerField(default=0)
    page_size = IntegerField(default=10)


class ActionSerializer(BaseSerializer):
    actor = CharField(source='actor_username')
    created_at = DateTimeField()
    id = CharField()  # pylint: disable=invalid-name
    verb = CharField()
    object = CharField()
    target = CharField(source='target_username')

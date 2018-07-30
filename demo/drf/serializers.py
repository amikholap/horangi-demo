from rest_framework.serializers import Serializer


class BaseSerializer(Serializer):

    def create(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """Mute pylint abstract method warnings."""
        pass

    def update(self, *args, **kwargs):  # pylint: disable=arguments-differ
        """Mute pylint abstract method warnings."""
        pass

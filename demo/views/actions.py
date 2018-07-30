from demo.core.controllers.action import ActionController
from demo.drf.response import DemoResponse
from demo.drf.views import DemoAPIView
from ..serializers.actions import (
    ActionArgumentsSerializer, ActionSerializer, RelatedActionListArgumentSerializer,
)


class BaseActionAPIView(DemoAPIView):
    controller = ActionController.from_settings()


class ActionListAPIView(BaseActionAPIView):

    arguments_serializer_class = ActionArgumentsSerializer

    def do_post(self, request):
        # An improvement would be to pass action id from client to enable idempotent retries.

        data = None
        error = None

        try:
            action = self.controller.create_action(
                actor=request.arguments['actor'],
                verb=request.arguments['verb'],
                object_=request.arguments['object'],
                target=request.arguments['target'],
            )
        except self.controller.Error as e:
            error = e.code

        if error is None:
            data = ActionSerializer(action).data

        return DemoResponse(data=data, errors=error)


class RelatedActionListAPIView(BaseActionAPIView):

    arguments_serializer_class = RelatedActionListArgumentSerializer

    def do_get(self, request):
        related_actions = self.controller.action_dp.list_related(
            object_=request.arguments['object'],
            exclude_username=request.arguments['username'],
        )
        return DemoResponse(related_actions)

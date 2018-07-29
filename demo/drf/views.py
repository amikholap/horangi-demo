from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView

from .response import DemoResponse


class DemoAPIView(APIView):

    arguments_serializer_class = None

    def do_get(self, request):
        raise NotImplementedError

    def do_post(self, request):
        raise NotImplementedError

    def get(self, request):
        try:
            arguments = self._get_arguments(request)
        except ValidationError as e:
            return self._render_validation_error(e)

        request.arguments = arguments

        response = self.do_get(request)

        return response

    def post(self, request):
        try:
            arguments = self._get_arguments(request)
        except ValidationError as e:
            return self._render_validation_error(e)

        request.arguments = arguments

        response = self.do_post(request)

        return response

    def get_arguments_serializer_class(self, request):
        return self.arguments_serializer_class

    def _get_arguments(self, request):
        arguments = None
        serializer_class = self.get_arguments_serializer_class(request)
        if serializer_class is not None:
            serializer = serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            arguments = serializer.data
        return arguments

    def _render_validation_error(self, exc):
        error_codes = []
        for key, codes in exc.get_codes().items():
            for code in codes:
                error_code = '{}.{}'.format(key, code)
                error_codes.append(error_code)
        return DemoResponse(errors=error_codes)

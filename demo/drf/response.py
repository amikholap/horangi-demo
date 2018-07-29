from rest_framework.response import Response


class DemoResponse(Response):

    def __init__(self, data=None, errors=None, **kwargs):
        if errors is not None:
            data = {
                'status': 'error',
                'errors': errors,
                'data': None,
            }
        else:
            data = {
                'status': 'success',
                'data': data,
            }
        super().__init__(data=data, **kwargs)

import json

import django.http


class API(object):
    @staticmethod
    def _response(data):
        return django.http.HttpResponse(data, content_type='application/json')

    @classmethod
    def tasks_list(cls, request):
        return cls._response(json.dumps({}))

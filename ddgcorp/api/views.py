import json

import django.http

import ddgcorp.models


class API(object):
    @staticmethod
    def _response(data):
        return django.http.HttpResponse(data, content_type='application/json')

    @classmethod
    def task(cls, request, pk):
        obj = ddgcorp.models.Task.objects.filter(pk=pk).first()
        if not obj:
            raise django.http.Http404('Task {} does not exist'.format(pk))
        return cls._response(json.dumps(obj.to_dict()))

    @classmethod
    def tasks(cls, request):
        objs = [o.to_dict() for o in ddgcorp.models.Task.objects.all()]
        return cls._response(json.dumps(objs))

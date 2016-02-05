import json

import django.http

from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

import ddgcorp.models


class API(object):
    @staticmethod
    def _response(data):
        return django.http.HttpResponse(data, content_type='application/json')

    @classmethod
    def last_modified(cls, request):
        """
        """
        status_last_modified = ddgcorp.models.Status.get_last_modify_timestamp()
        task_last_modified = ddgcorp.models.Task.get_last_modify_timestamp()
        last_modified = max(status_last_modified, task_last_modified)
        return cls._response(json.dumps({'timestamp': last_modified}))

    @classmethod
    def statuses(cls, request):
        ret = [o.to_dict() for o in ddgcorp.models.Status.objects.all()]
        return cls._response(json.dumps(ret))

    #@require_http_methods(['GET'])
    @classmethod
    def task(cls, request, pk):
        obj = ddgcorp.models.Task.objects.filter(pk=pk).first()
        if not obj:
            raise django.http.Http404('Task {} does not exist'.format(pk))
        return cls._response(json.dumps(obj.to_dict()))

    #@require_http_methods(['PUT'])
    @classmethod
    @csrf_exempt
    def task_status(cls, request, pk):
        data = json.loads(request.body)
        new_status_id = data['new_status_id']
        obj = ddgcorp.models.Task.objects.filter(pk=pk).first()
        if not obj:
            raise django.http.Http404('Task {} does not exist'.format(pk))
        # update status
        status = ddgcorp.models.Status.objects.filter(pk=new_status_id).first()
        if not status:
            raise django.http.Http404('Status {} does not exist'.format(new_status_id))
        obj.status = status
        obj.save()
        #
        return cls._response(json.dumps({}))

    #@require_http_methods(['GET'])
    @classmethod
    def tasks(cls, request):
        ret = [o.to_dict() for o in ddgcorp.models.Task.objects.all()]
        return cls._response(json.dumps(ret))

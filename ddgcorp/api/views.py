import json

import django.http

from django.views.decorators.http import require_http_methods

import ddgcorp.models


@require_http_methods(['GET'])
def statuses(_):
    """
    REST: /api/status/
    """
    objs = ddgcorp.models.Status.all()
    return django.http.JsonResponse(objs, safe=False)


@require_http_methods(['GET'])
def tasks(_):
    """
    REST: /api/task/
    """
    objs = ddgcorp.models.Task.all()
    return django.http.JsonResponse(objs, safe=False)


@require_http_methods(['GET'])
def task(_, pk):
    """
    REST: /api/task/<pk>/
    """
    obj = ddgcorp.models.Task.one(pk)
    if not obj:
        raise django.http.Http404(
            'Task {} does not exist'.format(pk))
    return django.http.JsonResponse(obj)


@require_http_methods(['PUT'])
def task__status(request, pk):
    """
    REST: /api/task/<pk>/status
    data: {'status': status_id}
    """
    data = json.loads(request.body)
    if 'status' not in data:
        raise django.http.Http404('Invalid data')
    status_id = data['status']
    #
    try:
        ddgcorp.models.Task.update_status(pk, status_id)
    except ddgcorp.models.ModelsException as ex:
        raise django.http.Http404(ex.message)
    #
    return django.http.JsonResponse({})

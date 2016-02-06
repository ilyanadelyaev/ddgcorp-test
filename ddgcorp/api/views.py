import json

import django.http

from django.views.decorators.http import require_http_methods

import ddgcorp.models


@require_http_methods(['GET'])
def statuses(_):
    """
    REST: /api/status/
    """
    objs = [o.to_dict() for o in ddgcorp.models.Status.objects.all()]
    return django.http.JsonResponse(objs, safe=False)


@require_http_methods(['GET'])
def tasks(_):
    """
    REST: /api/task/
    """
    objs = [o.to_dict() for o in ddgcorp.models.Task.objects.all()]
    return django.http.JsonResponse(objs, safe=False)


@require_http_methods(['GET'])
def task(_, pk):
    """
    REST: /api/task/<pk>/
    """
    task_obj = ddgcorp.models.Task.objects.filter(pk=pk).first()
    if not task_obj:
        raise django.http.Http404(
            'Task {} does not exist'.format(pk))
    return django.http.JsonResponse(task_obj.to_dict())


@require_http_methods(['PUT'])
def task__status(request, pk):
    """
    REST: /api/task/<pk>/status
    data: {'status': status_id}
    """
    data = json.loads(request.body)
    if 'status' not in data:
        raise django.http.Http404('Invalid data')
    # get task
    task_obj = ddgcorp.models.Task.objects.filter(pk=pk).first()
    if not task_obj:
        raise django.http.Http404(
            'Task {} does not exist'.format(pk))
    # get new status
    status_id = data['status']
    status_obj = ddgcorp.models.Status.objects.filter(pk=status_id).first()
    if not status_obj:
        raise django.http.Http404(
            'Status {} does not exist'.format(status_id))
    # update status
    task_obj.status = status_obj
    task_obj.save()
    #
    return django.http.JsonResponse({})

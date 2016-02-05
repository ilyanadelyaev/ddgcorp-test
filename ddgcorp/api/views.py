import json

import django.http

from django.views.decorators.http import require_http_methods

import ddgcorp.models


@require_http_methods(['GET'])
def statuses(request):
    """
    REST: /api/status/
    """
    objs = [o.to_dict() for o in ddgcorp.models.Status.objects.all()]
    return django.http.JsonResponse(objs, safe=False)


@require_http_methods(['GET'])
def tasks(request):
    """
    REST: /api/task/
    """
    objs = [o.to_dict() for o in ddgcorp.models.Task.objects.all()]
    return django.http.JsonResponse(objs, safe=False)


@require_http_methods(['GET'])
def task(request, pk):
    """
    REST: /api/task/<pk>/
    """
    task = ddgcorp.models.Task.objects.filter(pk=pk).first()
    if not task:
        raise django.http.Http404('Task {} does not exist'.format(pk))
    return django.http.JsonResponse(task.to_dict())


@require_http_methods(['PUT'])
def task__status(request, pk):
    """
    REST: /api/task/<pk>/status
    data: {'status': new_status}
    """
    data = json.loads(request.body)
    if 'status' not in data:
        raise django.http.Http404('Invalid data')
    # get task
    task = ddgcorp.models.Task.objects.filter(pk=pk).first()
    if not task:
        raise django.http.Http404('Task {} does not exist'.format(pk))
    # get new status
    new_status = data['status']
    status = ddgcorp.models.Status.objects.filter(pk=new_status).first()
    if not status:
        raise django.http.Http404('Status {} does not exist'.format(new_status))
    # update status
    task.status = status
    task.save()
    #
    return django.http.JsonResponse({})


@require_http_methods(['GET'])
def handle__last_modified(request):
    """
    HANDLE: /api/handle/last_modified
    get last database modification timestamp
    """
    models_to_check = (
        ddgcorp.models.Status,
        ddgcorp.models.Task,
    )
    # get max timestamp from selected models
    timestamps = []
    for model in models_to_check:
        timestamps.append(model.get_last_modify_timestamp())
    #
    return django.http.JsonResponse({'timestamp': max(timestamps)})

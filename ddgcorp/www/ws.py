import json

import django.db.models.signals
import django.dispatch
import ws4redis.publisher
import ws4redis.redis_store

import ddgcorp.models


# signals

models_publisher = ws4redis.publisher.RedisPublisher(
    facility='models', broadcast=True)


def __statuses():
    return [o.to_dict() for o in ddgcorp.models.Status.objects.all()]


def __tasks():
    return [o.to_dict() for o in ddgcorp.models.Task.objects.all()]


@django.dispatch.receiver(
    (
        django.db.models.signals.post_save,
        django.db.models.signals.post_delete,
    ),
    sender=ddgcorp.models.Status,
    dispatch_uid='status_change_signal_processor'
)
# pylint: disable=W0613
def status_change_signal_processor(sender, instance, **kwargs):
    """
    Fires on Status model change or delete
    Send all statuses to queue
    """
    data = {
        'model': 'status',
        'change': instance.to_dict(),
        'objects': __statuses(),
    }
    message = ws4redis.redis_store.RedisMessage(json.dumps(data))
    models_publisher.publish_message(message)


@django.dispatch.receiver(
    (
        django.db.models.signals.post_save,
        django.db.models.signals.post_delete,
    ),
    sender=ddgcorp.models.Task,
    dispatch_uid='task_change_signal_processor',
)
# pylint: disable=W0613
def task_change_signal_processor(sender, instance, **kwargs):
    """
    Fires on Task model change or delete
    Send all tasks to queue
    """
    data = {
        'model': 'task',
        'change': instance.to_dict(),
        'objects': __tasks(),
    }
    message = ws4redis.redis_store.RedisMessage(json.dumps(data))
    models_publisher.publish_message(message)

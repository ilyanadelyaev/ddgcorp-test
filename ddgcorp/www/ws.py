import json

import django.db.models.signals
import django.dispatch
import ws4redis.publisher
import ws4redis.redis_store

import ddgcorp.models


# signals

models_publisher = ws4redis.publisher.RedisPublisher(
    facility='models', broadcast=True)


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
    signal = kwargs['signal']
    if signal == django.db.models.signals.post_save:
        action = 'save'
    elif signal == django.db.models.signals.post_delete:
        action = 'delete'
    else:
        return
    data = {
        'type': 'status',
        'action': action,
        'model': instance.to_dict(),
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
    signal = kwargs['signal']
    if signal == django.db.models.signals.post_save:
        action = 'save'
    elif signal == django.db.models.signals.post_delete:
        action = 'delete'
    else:
        return
    data = {
        'type': 'task',
        'action': action,
        'model': instance.to_dict(),
    }
    message = ws4redis.redis_store.RedisMessage(json.dumps(data))
    models_publisher.publish_message(message)

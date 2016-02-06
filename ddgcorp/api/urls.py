import django.conf.urls

import ddgcorp.api.views


urlpatterns = [
    django.conf.urls.url(
        r'^status/$',
        ddgcorp.api.views.statuses,
        name='statuses'
    ),
    django.conf.urls.url(
        r'^task/$',
        ddgcorp.api.views.tasks,
        name='tasks'
    ),
    django.conf.urls.url(
        r'^task/(?P<pk>[0-9]+)/$',
        ddgcorp.api.views.task,
        name='task'
    ),
    django.conf.urls.url(
        r'^task/(?P<pk>[0-9]+)/status/$',
        ddgcorp.api.views.task__status,
        name='task__status'
    ),
]

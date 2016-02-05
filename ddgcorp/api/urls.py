import django.conf.urls

import ddgcorp.api.views


urlpatterns = [
    # REST
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

    # handles
    django.conf.urls.url(
        r'^handle/last_modified$',
        ddgcorp.api.views.handle__last_modified,
        name='handle__last_modified'
    ),
]

import django.conf.urls

import ddgcorp.api.views


urlpatterns = [
    # handlers
    django.conf.urls.url(
        r'^last_modified$',
        ddgcorp.api.views.API.last_modified,
        name='last_modified'),
    # REST
    django.conf.urls.url(
        r'^status/$',
        ddgcorp.api.views.API.statuses,
        name='statuses'),
    django.conf.urls.url(
        r'^task/(?P<pk>[0-9]+)/$',
        ddgcorp.api.views.API.task,
        name='task'),
    django.conf.urls.url(
        r'^task/(?P<pk>[0-9]+)/status/$',
        ddgcorp.api.views.API.task_status,
        name='task_status'),
    django.conf.urls.url(
        r'^task/$',
        ddgcorp.api.views.API.tasks,
        name='tasks'),
]

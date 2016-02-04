import django.conf.urls

import ddgcorp.api.views


urlpatterns = [
    django.conf.urls.url(
        r'^task/(?P<pk>[0-9]+)/$',
        ddgcorp.api.views.API.task,
        name='task'),
    django.conf.urls.url(
        r'^task/$',
        ddgcorp.api.views.API.tasks,
        name='tasks'),
]

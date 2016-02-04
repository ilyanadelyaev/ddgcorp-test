import django.conf.urls

import ddgcorp.api.views


urlpatterns = [
    django.conf.urls.url(
        r'^task/$',
        ddgcorp.api.views.API.tasks_list,
        name='tasks_list'),
]

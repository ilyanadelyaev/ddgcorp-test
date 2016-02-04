import django.conf.urls

import ddgcorp.www.views


urlpatterns = [
    django.conf.urls.url(
        r'^$',
        ddgcorp.www.views.index,
        name='index'),
]

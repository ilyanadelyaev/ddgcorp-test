import django.conf.urls
import django.views.generic

# Register WebSocket models signals
# pylint: disable=W0611
import ddgcorp.www.ws


urlpatterns = [
    django.conf.urls.url(
        r'^$',
        django.views.generic.TemplateView.as_view(
            template_name='www/index.html'),
        name='index'
    ),
]

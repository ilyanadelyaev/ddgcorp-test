import django.conf.urls
import django.views.generic


urlpatterns = [
    django.conf.urls.url(
        r'^$',
        django.views.generic.TemplateView.as_view(
            template_name='www/index.html'),
        name='index'
    ),
]

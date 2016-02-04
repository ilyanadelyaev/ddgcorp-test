from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('ddgcorp.www.urls', namespace='www')),
    url(r'^api/', include('ddgcorp.api.urls', namespace='api')),
    #
    url(r'^admin/', admin.site.urls),
]

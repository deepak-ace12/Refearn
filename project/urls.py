from django.conf.urls import include, url
from django.contrib import admin
from refearn.views import CustomerViewSet
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='refearn/index.html')),
    url(r'^api/', include('refearn.urls')),
]

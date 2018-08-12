from django.conf.urls import include, url
from django.contrib import admin
from refearn.views import CustomerViewSet
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^', admin.site.urls),
    url(r'^api/', include('refearn.urls')),
]

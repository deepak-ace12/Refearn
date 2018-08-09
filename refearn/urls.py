
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from refearn.views import *
from django.views.generic import TemplateView


app_name = 'refearn'
router = DefaultRouter()
router.register(r'customer', CustomerViewSet)
router.register(r'refferal', CustomerReferralView)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^customer/(?P<customer_id>[0-9]+)/children/$', CustomerChildrenView.as_view()),
    url(r'^add/refferal/$', TemplateView.as_view(template_name='refearn/refferal.html')),
]
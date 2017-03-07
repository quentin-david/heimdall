from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from .models import Foreman

urlpatterns = [
    url(r'foreman$', login_required(views.ForemanList.as_view()), name='foreman_list'),
    url(r'foreman/new$', login_required(views.ForemanCreate.as_view()), name='foreman_create'),
    url(r'foreman/edit/(?P<pk>\d+)$', login_required(views.ForemanUpdate.as_view()), name='foreman_update'),
]
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', login_required(views.visioHome), name='visio_home'),
    url(r'^video$', views.visioVideo, name='visio_video'),
]
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from .models import Bugzilla

urlpatterns =[
    #url(r'^$', views.BugzillaList.as_view(), name='bugzilla_list'),
    url(r'^$', login_required(views.BugzillaSearchList.as_view()), name='bugzilla_list'),
    url(r'new$', login_required(views.bugzillaCreate), name='bugzilla_create'),
    url(r'edit/(?P<pk>\d+)$', login_required(views.BugzillaUpdate.as_view()), name='bugzilla_update'),
]
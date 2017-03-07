from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
#from .models import Monitoring

urlpatterns = [
    # Munin
    url(r'^$', login_required(views.monitoringHome), name='monitoring_home'),
    url(r'munin/new$', login_required(views.MuninCreate.as_view()), name='munin_create'),
    url(r'munin/edit/(?P<pk>\d+)$', login_required(views.MuninUpdate.as_view()), name='munin_update'),
    # Munin API calls
    url(r'munin/png/(?P<node_or_host>\w+)/(?P<node_id>\d+)/(?P<resource_type>\w+)/(?P<resource_time>\w+)$', views.muninPic, name='pic'),
    # Munin graphs
    url(r'munin/node/(?P<node_id>\d+)/(?P<resource_time>\w+)$', login_required(views.muninNodeView), name='munin_node_view'),
    url(r'munin/host/(?P<host_id>\d+)/(?P<resource_time>\w+)$', login_required(views.muninHostView), name='munin_host_view'),
    # Profiling
    url(r'munin/profiling/(?P<host_id>\d+)/(?P<metric>\w+)/(?P<precision>\w+)$', login_required(views.muninProfiling), name='munin_profiling'),
]

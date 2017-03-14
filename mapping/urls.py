from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from .models import Application, Host, ServiceWebServer

urlpatterns = [
    # Applications
    url(r'app$', login_required(views.ApplicationList.as_view()), name='application_list'),
    url(r'app/new$', login_required(views.ApplicationCreate.as_view()), name='application_create'),
    #url(r'app/(?P<pk>\d+)$', login_required(views.ApplicationView.as_view()), name='application_view'),
    url(r'app/(?P<appli_id>\d+)$', login_required(views.applicationView), name='application_view'),
    url(r'app/edit/(?P<pk>\d+)$', login_required(views.ApplicationUpdate.as_view()), name='application_update'),
    url(r'app/delete/(?P<pk>\d+)$', login_required(views.ApplicationDelete.as_view()), name='application_delete'),
    # Hosts
    url(r'host$', login_required(views.hostList), name='host_list'),
    url(r'host/new$', login_required(views.HostCreate.as_view()), name='host_create'),
    url(r'host/(?P<id>\d+)$', login_required(views.hostView), name='host_view'),
    url(r'host/edit/(?P<pk>\d+)', login_required(views.HostUpdate.as_view()), name='host_update'),
    url(r'host/delete/(?P<pk>\d+)$', login_required(views.HostDelete.as_view()), name='host_delete'),
    url(r'host/(?P<host_id>\d+)/set_nodes_params$', login_required(views.hostSetAllNodesParamsFromForeman), name='host_set_nodes_params'),
     # Nodes
    url(r'host/(?P<host_id>\d+)/(?P<foreman_node_id>\d+)$', views.hostCreateNode, name='host_create_node'),
    url(r'host/(?P<host_id>\d+)/create_unregistered_nodes$', views.hostCreateAllUnregisteredNodes, name='host_create_unregistered_nodes'),
    url(r'node/(?P<pk>\d+)$', views.nodeView, name='node_view'),
    url(r'node/delete/(?P<pk>\d+)$', login_required(views.NodeDelete.as_view()), name='node_delete'),
    #url(r'node/edit/(?P<pk>\d+)$', login_required(views.NodeUpdate.as_view()), name='node_update'),
    url(r'node/edit/(?P<node_id>\d+)$', login_required(views.nodeCreateOrUpdate), name='node_update'),
    url(r'node/(?P<node_id>\d+)/set_params$', views.nodeSetParamsFromForeman, name='node_set_params'),
    #url(r'^node/new$', login_required(views.NodeCreate.as_view()), name='node_create'),
    url(r'^node/new$', login_required(views.nodeCreateOrUpdate), name='node_create'),
    # Networks
    url(r'network$', views.networkList, name='network_list'),
    url(r'network/new$', views.NetworkCreate.as_view(), name='network_create'),
    # Services
    url(r'^service$', login_required(views.ServiceList.as_view()), name='service_list'),
    
    url(r'node/(?P<application_id>\d+)/service/new/webserver$', views.serviceWebServerCreate, name='service_webserver_create'),
    url(r'node/(?P<application_id>\d+)/service/webserver/edit/(?P<webserver_id>\d+)$', login_required(views.serviceWebServerUpdate), name='service_webserver_update'),
    url(r'node/(?P<application_id>\d+)/service/delete/(?P<pk>\d+)$', login_required(views.ServiceDelete.as_view()), name='service_delete'),
    
    url(r'node/(?P<application_id>\d+)/service/new/reverseproxy$', views.serviceReverseProxyCreate, name='service_reverseproxy_create'),
    url(r'node/(?P<application_id>\d+)/service/reverseproxy/edit/(?P<reverseproxy_id>\d+)$', login_required(views.serviceReverseProxyUpdate), name='service_reverseproxy_update'),
    
    url(r'node/(?P<application_id>\d+)/service/new/database$', views.serviceDatabaseCreate, name='service_database_create'),

]
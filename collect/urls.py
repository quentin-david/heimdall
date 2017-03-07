from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^$', login_required(views.collectHome), name='collect_home'),
    url(r'profile/new$', login_required(views.CollectProfileCreate.as_view()), name='collect_profile_create'),
    url(r'profile/edit/(?P<pk>\d+)$', login_required(views.CollectProfileUpdate.as_view()), name='collect_profile_update'),
    url(r'item/new$', login_required(views.CollectItemCreate.as_view()), name='collect_item_create'),
    url(r'item/edit/(?P<pk>\d+)$', login_required(views.CollectItemUpdate.as_view()), name='collect_item_update'),
    # Collect
    url('purge$', login_required(views.purgeCollect), name='collect_purge'),
    url('node/(?P<node_id>\d+)/collect$', login_required(views.collectNode), name='collecting_node'),
    url('node/(?P<node_id>\d+)$', views.collectedElementsByNode, name='node_collect'),
    url('global$', views.collectEveryNode, name='collect_global'),
]
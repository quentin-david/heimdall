from django.shortcuts import render
from django.http import HttpResponse
from .models import Munin
from mapping.models import Node, Host, Application
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from .forms import MuninForm
from mapping.models import NetworkLink


def monitoringHome(request):
    munin_server_list = Munin.objects.all()
    host_list = Host.objects.all()
    application_list = Application.objects.all()
    metric_list = {'memory':'RAM', 'diskstats_iops': 'disk activity','load': 'load average','fw_packets':'network activity','cpu': 'CPU'}
    return render(request,'monitoring/monitoring.html', locals())

class MuninCreate(CreateView):
    model = Munin
    form_class = MuninForm
    template_name = 'munin/munin_create_form.html'
    success_url = reverse_lazy('monitoring_home')

class MuninUpdate(UpdateView):
    model = Munin
    form_class = MuninForm
    template_name = 'munin/munin_create_form.html'
    success_url = reverse_lazy('monitoring_home')


# Url to render a picture from Munin (asynchronous call)
def muninPic(request, node_or_host, node_id, resource_type,resource_time):
    # node_or_host = 'host' or 'node'
    if(node_or_host == 'node'):
        node = Node.objects.get(id=node_id)
    elif(node_or_host == 'host'):
        node = Host.objects.get(id=node_id)
    node_munin_name = node.name.split('.')[0]
    munin = node.munin_server
    pic = munin.getMuninPicture(node_munin_name,resource_type,resource_time)
    response = HttpResponse(pic,content_type="image/png")
    return response

# Graphs by nodes/hots
# All the graphs for one node
def muninNodeView(request,node_id,resource_time):
    node = Node.objects.get(id=node_id)
    
    metric_list = ['memory','diskstats_iops','load','fw_packets','cpu']
    metric_list_ok = []
    metric_list_ko = []
    for metric in metric_list:
        if node.munin_server.getMuninPicture(node.name.split('.')[0],metric,'day'):
            metric_list_ok.append(metric)
        else:
            metric_list_ko.append(metric)
    
    network_metric_list_ok = []
    network_metric_list_ko = []
    for nic in NetworkLink.objects.filter(node=node):
        for net_metric in ['if_', 'if_err_']:
            if node.munin_server.getMuninPicture(node.name.split('.')[0],net_metric+nic.iface,'day'):
                network_metric_list_ok.append(net_metric+nic.iface)
            else:
                network_metric_list_ko.append(net_metric+nic.iface)
    
    node_list = node.host.node_set.order_by('name')
    host_list = Host.objects.all()
    
    return render(request, 'munin/munin_node.html', locals())


# All the graphs for one host
def muninHostView(request,host_id,resource_time):
    host = Host.objects.get(id=host_id)
    metric_list = ['memory','diskstats_iops','load','fw_conntrack','cpu', 'if_eth0']
    node_list = host.node_set.order_by('name')
    host_list = Host.objects.all()
    return render(request,'munin/munin_host.html', locals())


# Profiling by type
def muninProfiling(request, host_id, metric, precision):
    host = Host.objects.get(id=host_id)
    metric_list = {'memory':'RAM', 'diskstats_iops': 'disk activity','load': 'load average','fw_packets':'network activity','cpu': 'CPU'}
    return render(request, 'munin/munin_profiling.html', {'host': host, 'metric': metric, 'precision':precision, 'metric_list':metric_list})


from django.shortcuts import render, redirect
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
import json
from .models import Application, Host, Node, Network, NetworkLink, ServiceWebServer, Service, ServiceReverseProxy, ServiceDatabase
from bugzilla.models import Bugzilla
from .forms import ApplicationForm, HostForm, NodeForm, NodeFullForm, NetworkForm, NetworkLinkForm, ServiceWebServerForm, ServiceReverseProxyForm, ServiceDatabaseForm
from deployment.models import Foreman
from collect.models import CollectItem, Collect
from django.conf import settings
from django.forms import modelformset_factory
from django.forms import formset_factory

"""
APPLICATIONS
"""
class ApplicationList(ListView):
    model = Application
    context_object_name = 'application_list'
    template_name = 'application/application_list.html'

class ApplicationCreate(CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'application/application_create_form.html'
    success_url = reverse_lazy('application_list')
    #Add the list of applications to display on the left panel
    def get_context_data(self, **kwargs):
        context = super(ApplicationCreate, self).get_context_data(**kwargs)
        context['application_list'] = Application.objects.all()
        return context

"""
class ApplicationView(DetailView):
    model = Application
    context_object_name = 'appli'
    template_name = 'application/application.html'
    #Add the list of applications to display on the left panel
    def get_context_data(self, **kwargs):
        context = super(ApplicationView, self).get_context_data(**kwargs)
        context['application_list'] = Application.objects.all()
        context['network_list'] = Network.objects.all()
        #context['servicewebserver_list'] = ServiceWebServer.objects.filter(application=self.appli)
        return context
"""
def applicationView(request, appli_id):
    appli = Application.objects.get(id=appli_id)
    application_list = Application.objects.all()
    network_list = Network.objects.all()
    bugzilla_opened_list = Bugzilla.objects.filter(application=appli,state="open")
    servicewebserver_list = ServiceWebServer.objects.filter(application=appli)
    servicereverseproxy_list = ServiceReverseProxy.objects.filter(application=appli)
    servicedatabase_list = ServiceDatabase.objects.filter(application=appli)
    #form_webserver = ServiceWebServerForm(request.POST or None,request.FILES or None, application=appli)
    #form_reverseproxy = ServiceReverseProxyForm(request.POST or None,request.FILES or None, application=appli)
    #form_database = ServiceDatabaseForm(request.POST or None,request.FILES or None, application=appli)
    creation_from_heimdall = settings.CREATE_NODE_FROM_HEIMDALL
    
    return render(request, 'application/application.html', locals())

class ApplicationUpdate(UpdateView):
    model = Application
    form_class = ApplicationForm
    template_name = 'application/application_create_form.html'
    #success_url = reverse_lazy('application_list')
    #Add the list of applications to display on the left panel
    def get_context_data(self, **kwargs):
        context = super(ApplicationUpdate, self).get_context_data(**kwargs)
        context['application_list'] = Application.objects.all()
        return context
    
class ApplicationDelete(DeleteView):
    model = Application
    context_object_name = 'appli'
    template_name = 'application/application_delete.html'
    success_url = reverse_lazy('application_list')



"""
##################################   HOSTS   ########################################
"""
def hostList(request):
    host_list = Host.objects.all()
    
    return render(request, 'host/host_list.html', {'host_list':host_list})

class HostCreate(CreateView):
    model = Host
    form_class = HostForm
    template_name = 'host/host_create_form.html'
    success_url = reverse_lazy('host_list')

"""
hostView : Host details + list of attached nodes (guests)
"""
def hostView(request, id):
    host = Host.objects.get(id=id)
    node_list = host.node_set.order_by('application')
    foreman = host.foreman_server
    foreman_nodes_list = foreman.getNodeListByHost(host.name)
    foreman_nodes_unregistered = []
    if(foreman_nodes_list):
        foreman_nodes_unregistered = host.checkNodeListFromForeman(foreman_nodes_list)
    
    return render(request, 'host/host.html', {'host': host,'foreman_nodes_unregistered': foreman_nodes_unregistered,'node_list': node_list})
    
    
class HostUpdate(UpdateView):
    model = Host
    form_class = HostForm
    template_name = 'host/host_create_form.html'
    success_url = reverse_lazy('host_list')
    
    
class HostDelete(DeleteView):
    model = Host
    context_object_name = 'host'
    template_name = 'host/host_delete.html'
    success_url = reverse_lazy('host_list')
    
def hostCreateNode(request,host_id,foreman_node_id):
    Node().createNodeFromForeman(host_id,foreman_node_id)
    return redirect('host_view', id=host_id)

def hostCreateAllUnregisteredNodes(request,host_id):
    host = Host.objects.get(id=host_id)
    host.createAllNodesUnregistered()
    return redirect('host_view', id=host_id)

def hostSetAllNodesParamsFromForeman(request, host_id):
    host = Host.objects.get(id=host_id)
    host.setAllNodesParamsFromForeman()
    return redirect('host_view', id=host_id)



"""
###################################   NODES   ################################
"""
def nodeView(request, pk):
    node = Node.objects.get(id=pk)
    foreman = node.host.foreman_server
    node_foreman = foreman.getNodeByName(node.name) #debug
    if node_foreman:
        node_foreman_specs = foreman.getNodeVmSpecs(node_foreman['id']) #debug
    #node_foreman_service_list = node.getPuppetClassList()
    item = CollectItem.objects.filter(name='collect_script1')
    if node.collect_profile != None:
        collected_element = node.getNodeLastCollectItem()
        if collected_element:
            collected_data = json.loads(collected_element.data_json)
    
    return render(request, 'node/node.html', locals())



def nodeCreateOrUpdate(request, node_id=None, appli_id=None):
    application = Application.objects.get(id=appli_id)
    nb_networks = len(Network.objects.all())
    NetworkLinkFormFormset = modelformset_factory(NetworkLink, form=NetworkLinkForm, exclude=('node',) , extra=nb_networks)
    if node_id:
        node_to_edit = Node.objects.get(id=node_id)
        nb_networks = len(Network.objects.all()) - 3 + 1
        NetworkLinkFormFormset = modelformset_factory(NetworkLink, form=NetworkLinkForm, exclude=('node',) , extra=nb_networks)
        if node_to_edit.managed_by_heimdall:
            form = NodeFullForm(request.POST or None, instance=node_to_edit)
            template_name = 'node/node_full_create_form.html'
            network_link_form = NetworkLinkFormFormset(request.POST or None, queryset=NetworkLink.objects.filter(node=node_to_edit))
        else:
            form = NodeForm(request.POST or None, instance=node_to_edit)
            network_link_form = None
            template_name = 'node/node_create_form.html'
    else:
        nb_networks_extra = len(Network.objects.all())
        NetworkLinkFormFormset = modelformset_factory(NetworkLink, form=NetworkLinkForm, exclude=('node',) , extra=nb_networks_extra)
        network_link_form = NetworkLinkFormFormset(request.POST or None, queryset=NetworkLink.objects.none())
        form = NodeFullForm(request.POST or None, instance=None)
        template_name = 'node/node_full_create_form.html'
        
    if form.is_valid():
        node = form.save(commit=False)
        if node.application == '':
            node.application = application
        node.save()
        if network_link_form:
            if network_link_form.is_valid():
                #node.save()
                for net in network_link_form:
                    network = net.save(commit=False)
                    if network.ip != None:
                        network.node = node
                        network.save()
        return redirect('application_view', appli_id=node.application.id)
    return render(request, template_name, locals())


class NodeDelete(DeleteView):
    model = Node
    context_object_name = 'node'
    template_name = 'node/node_delete.html'
    success_url = reverse_lazy('host_list')


"""
def nodeUpdate(request, node_id):
    node = Node.objects.get(id=node_id)
    if node.managed_by_heimdall:
        form = NodeFullForm(request.POST or None, instance=node)
        template_name = 'node/node_full_create_form.html'
    else:
        form = NodeForm(request.POST or None, instance=node)
        template_name = 'node/node_create_form.html'
    if form.is_valid():
        node = form.save(commit=False)
        node.save()
        return redirect('application_view', appli_id=node.application.id)
    return render(request, template_name, locals())
"""

def nodeSetParamsFromForeman(request, node_id):
    node_to_copy = Node.objects.get(id=node_id)
    foreman = node_to_copy.host.foreman_server
    node_foreman = foreman.getNodeByName(node_to_copy.name)
    node_foreman_specs = foreman.getNodeVmSpecs(node_foreman['id'])
    # recreate the node with the Foreman parameters
    node_to_copy.createNode(node_foreman, node_foreman_specs, node_to_copy.host)
    return redirect('node_view', pk=node_id)
 
    



"""
#######################  Network  #############################
"""

def networkList(request):
    host_list = Host.objects.all()
    return render(request, 'network/network_list.html', {'host_list':host_list})

class NetworkCreate(CreateView):
    model = Network
    form_class = NetworkForm
    template_name = 'network/network_create_form.html'
    success_url = reverse_lazy('network_list') 





"""
#############################   Services   ##################################
"""
class ServiceList(ListView):
    model = Service
    context_object_name = 'service_list'
    template_name = 'service/service_list.html'
    def get_context_data(self, **kwargs):
        context = super(ServiceList, self).get_context_data(**kwargs)
        context['application_list'] = Application.objects.all()
        return context


class ServiceDelete(DeleteView):
    model = Service
    context_object_name = 'service'
    template_name = 'service/service_delete.html'
    success_url = reverse_lazy('application_list')
    
    
# Webserver
def serviceWebServerCreate(request, application_id):
    appli = Application.objects.get(id=application_id)
    form = ServiceWebServerForm(request.POST or None, application=appli)
    if form.is_valid():
        service = form.save(commit=False)
        service.application = appli
        service.save()
        return redirect('application_view', appli_id=application_id)
    return render(request, 'service/servicewebserver_create_form.html', locals())

def serviceWebServerUpdate(request, application_id, webserver_id):
    webserver = ServiceWebServer.objects.get(id=webserver_id)
    appli = Application.objects.get(id=application_id)
    form = ServiceWebServerForm(request.POST or None, instance=webserver, application=appli)
    if form.is_valid():
        form.save()
        return redirect('application_view', appli_id=application_id)
    return render(request, 'service/servicewebserver_create_form.html', locals())




# Reverse Proxy
def serviceReverseProxyCreate(request, application_id):
    appli = Application.objects.get(id=application_id)
    form = ServiceReverseProxyForm(request.POST or None, application=appli)
    if form.is_valid():
        service = form.save(commit=False)
        service.application = appli
        service.save()
        return redirect('application_view', appli_id=application_id)
    return render(request,'service/servicereverseproxy_create_form.html', locals())

def serviceReverseProxyUpdate(request, application_id, reverseproxy_id):
    appli = Application.objects.get(id=application_id)
    reverseproxy = ServiceReverseProxy.objects.get(id=reverseproxy_id)
    form = ServiceReverseProxyForm(request.POST or None, instance=reverseproxy, application=appli)
    if form.is_valid():
        form.save()
        return redirect('application_view', appli_id=application_id)
    return render(request,'service/servicereverseproxy_create_form.html', locals())  
    

# Database
def serviceDatabaseCreate(request, application_id):
    appli = Application.objects.get(id=application_id)
    form = ServiceDatabaseForm(request.POST or None, application=appli)
    if form.is_valid():
        service = form.save(commit=False)
        service.application = appli
        service.save()
        return redirect('application_view', appli_id=application_id)
    return render(request,'service/servicedatabase_create_form.html', locals())

def serviceDatabaseUpdate(request, application_id, database_id):
    appli = Application.objects.get(id=application_id)
    database = ServiceDatabase.objects.get(id=database_id)
    form = ServiceDatabaseForm(request.POST or None, instance=database, application=appli)
    if form.is_valid():
        form.save()
        return redirect('application_view', appli_id=application_id)
    return render(request,'service/servicedatabase_create_form.html', locals())  

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import json
import requests
import concurrent.futures
import datetime
from monitoring.models import Munin
from deployment.models import Foreman
from collect.models import Collect, CollectItem

"""
Application level > Node level
"""
class Application(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(null=True, blank=True)
    identifier = models.CharField(max_length=3, unique=True)
    owner = models.ForeignKey(User, blank=True, null=True)
    
    class Meta:
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('application_view', kwargs={'pk': self.pk})
    
    def getPublicURL(self):
        url_list = []
        for service in self.service_set.all():
            if service.servicewebserver and service.servicewebserver.reverse_proxy:
                url_list.append(service.servicewebserver.protocol+'://'+service.servicewebserver.servername+'.'+service.servicewebserver.reverse_proxy.proxy_url)
        return url_list    
        
"""
Abstract class Vms for Node and Host
"""
class Vm(models.Model):
    name = models.CharField(max_length=20, unique=True)
    description = models.TextField(null=True, blank=True)
    nb_ram = models.BigIntegerField()
    nb_cpu = models.BigIntegerField()
    os = models.CharField(max_length=50, null=True, blank=True)
    disk_size = models.IntegerField()
    munin_server = models.ForeignKey('monitoring.Munin', blank=True, null=True)
    
    class Meta:
        abstract = True
        
"""
Host (hyperviseur)
"""
class Host(Vm):
    ip_public = models.GenericIPAddressField()
    mac_public = models.CharField(max_length=21)
    foreman_server = models.ForeignKey('deployment.Foreman')

    def __str__(self):
        return self.name

    # Compare 2 lists of nodes
    # return : (only_in_foreman_list, only_in_heimdall_list,) both_in_list
    def checkNodeListFromForeman(self,foreman_node_list):
        both_in_list = []
        only_in_foreman_list = []
        for f_host in foreman_node_list:
            for host in self.node_set.all():
                if(f_host['name'] == host.name):
                    both_in_list.append(f_host) #list of nodes registered
        for f_host in foreman_node_list:
            if(f_host not in both_in_list):
                only_in_foreman_list.append(f_host)
        return only_in_foreman_list
    
    def createAllNodesUnregistered(self):
        foreman = self.foreman_server
        foreman_nodes_list = foreman.getNodeListByHost(self.name)
        if(foreman_nodes_list):
            foreman_nodes_unregistered = self.checkNodeListFromForeman(foreman_nodes_list)
            for node in foreman_nodes_unregistered:
                Node().createNodeFromForeman(self.id,node['id'])
        else:
            return False
    
    def setAllNodesParamsFromForeman(self):
        foreman = self.foreman_server
        for node in self.node_set.all():
            node_foreman = foreman.getNodeByName(node.name)
            node.createNodeFromForeman(node.host.id, node_foreman['id'])
    
    def getProvisionnedRam(self):
        total_provisionned = 0
        for node in self.node_set.all():
            total_provisionned += node.nb_ram
        return total_provisionned
    
    def getProvisionnedDisk(self):
        total_provisionned = 0
        for node in self.node_set.all():
            total_provisionned += node.disk_size
        return total_provisionned
    
"""
Node (VM), only Heimdall infos
"""
class Node(Vm):
    short_description = models.CharField(max_length=150, null=True, blank=True)
    application = models.ForeignKey(Application, blank=True, null=True)
    host = models.ForeignKey(Host, blank=True, null=True)
    date_check_foreman = models.DateTimeField(auto_now=True)
    date_update_foreman = models.DateTimeField(auto_now=True)
    ip_public = models.GenericIPAddressField(null=True, blank=True)
    ip_admin = models.GenericIPAddressField(null=True, blank=True)
    states = (('UN', 'Unknown'),('KO', 'KO'),('OK','OK'))
    state = models.CharField(max_length=2, choices=states, default='UN')
    foreman_status_label = models.CharField(max_length=10, blank=True,null=True)
    nb_nics = models.IntegerField(default=0)
    network_links = models.ManyToManyField('mapping.Network', through='NetworkLink', through_fields=('node','network') , blank=True)
    collect_profile = models.ForeignKey('collect.CollectProfile', null=True, blank=True)
    is_collected = models.BooleanField(default=True)
    managed_by_heimdall = models.BooleanField(default=False)
    
    class Meta:
        #ordering = ['-date_check_foreman']
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def createNode(self,foreman_object,foreman_object_specs,host):
        default_application = Application.objects.get(id=3) #
        self.name = foreman_object['name']
        self.application = default_application # bricolage
        if self.description == None:
            self.description = 'created from Foreman'
        else:
            self.description = self.description
        if self.short_description == None:
            self.short_description = 'created from Foreman'
        else:
            self.short_description = self.short_description
        self.host = host
        self.date_update_foreman = datetime.datetime.now()
        self.ip_admin = foreman_object['ip']
        self.nb_ram = foreman_object_specs['memory']
        self.nb_cpu = foreman_object_specs['cpus']
        self.disk_size = foreman_object_specs['volumes_attributes']['0']['capacity']
        self.os = foreman_object['operatingsystem_name']
        self.state = 'OK'
        self.foreman_status_label = foreman_object['global_status_label']
        self.save()
        self.setParamsNicsFromForeman(foreman_object, foreman_object_specs)
        

    def createNodeFromForeman(self,host_id,foreman_node_id):
        host = Host.objects.get(id=host_id)
        foreman = host.foreman_server
        foreman_node = foreman.getNode(foreman_node_id)
        foreman_node_specs = foreman.getNodeVmSpecs(foreman_node['id'])
        self.createNode(foreman_node,foreman_node_specs,host)    
    
   
    def setParamsNicsFromForeman(self,foreman_object, foreman_object_specs):
        for nic in foreman_object_specs['nics']:
            if('network' in nic):
                net = Network.objects.get(name=nic['network'])
            else:
                net = Network.objects.get(name='public')
            nic_type = nic['model']
            current_ip = ''
            current_dev = ''
            current_nic_type = ''
            for iface in foreman_object['interfaces']:
                if(iface['mac'] == nic['mac']):
                    current_ip = iface['ip']
                    current_dev = iface['identifier']
            if(len(NetworkLink.objects.filter(node=self.id, network=net)) == 0):      
                NetworkLink.objects.create(node=self,network=net,mac=nic['mac'],ip=current_ip,iface=current_dev,nic_type=nic_type)
            else:
                NetworkLink.objects.get(node=self.id, network=net).delete()
                NetworkLink.objects.create(node=self,network=net,mac=nic['mac'],ip=current_ip,iface=current_dev,nic_type=nic_type)
    
    def getCollectedElements(self):
        #item = CollectItem.objects.filter(name='collect_script1')
        collected_element = Collect().getLastCollectItemByNode()
        return collected_element
    
    """
    def getPuppetClassList(self):
        foreman = self.host.foreman_server
        puppet_class_list = []
        for puppet_class in foreman.getNodeByName(self.name)['puppetclasses']:
            puppet_element = {}
            puppet_element['name'] = foreman.getPuppetClass(puppet_class['id'])['name']
            puppet_class_list.append(puppet_element)
        return puppet_class_list
    """
    
    """
    get every last element collected for a node
    """
    def getNodeLastCollect(self):
        item_list = Collect.objects.values('item').filter(node=self).distinct('item')
        file_list = []
        for item in item_list:
            file_list.append(Collect.objects.filter(node=self,item=item['item']).latest())
        return file_list
    
    """
    get last given item of a node
    """
    def getNodeLastCollectItem(self):
        item = CollectItem.objects.get(name='collect_script1') # QT constante a sup'
        try:
            collects = Collect.objects.filter(node=self,item=item).latest()
        except Collect.DoesNotExist:
            collects = False
        return collects
    
    

"""
Network
"""
class Network(models.Model):
    name = models.CharField(max_length=20)
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name+' over '+self.host.name


class NetworkLink(models.Model):
    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    node = models.ForeignKey(Node, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(null=True, blank=True)
    mac = models.CharField(max_length=20, null=True, blank=True)
    iface = models.CharField(max_length=20, default='ens', null=True, blank=True)
    nic_type = models.CharField(max_length=20, default='virtio', null=True, blank=True)




"""
Service
"""
class Service(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(null=True, blank=True)
    node = models.ForeignKey(Node, on_delete=models.CASCADE, null=True, blank=True)
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class ServiceReverseProxy(Service):
    servername = models.CharField(max_length=30, null=True, blank=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    port = models.IntegerField(null=True)
    proxy_url = models.CharField(max_length=50,null=True, blank=True)
    families = (('apache','apache'),)
    family = models.CharField(max_length=20, choices=families, default='apache')
    protocols = (('http','http'),('https','https'),)
    protocol = models.CharField(max_length=20, choices=protocols, default='http')
    
    def getAttachedApplications(self):
        return self.servicewebserver_set.all()
      

class ServiceWebServer(Service):
    servername = models.CharField(max_length=30)
    ip = models.GenericIPAddressField(null=True, blank=True)
    port = models.IntegerField(null=True)
    families = (('apache','apache'),)
    family = models.CharField(max_length=20, choices=families, default='apache')
    protocols = (('http','http'),('https','https'),)
    protocol = models.CharField(max_length=20, choices=protocols, default='http')
    url_root = models.CharField(max_length=50, null=True, blank=True, default=' ')
    reverse_proxy = models.ForeignKey(ServiceReverseProxy)
    
    def getFQDN(self):
        return str(self.reverse_proxy.protocol)+'://'+str(self.servername)+'.'+str(self.reverse_proxy.proxy_url)+'/'+str(self.url_root)

    def isOnline(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            if not self.port:
                url = 'http://'+self.ip+'/'
            else:
                url = 'http://'+self.ip+':'+str(self.port)+'/'
            cmd = executor.submit(requests.get, url, verify=False)
            try:
                data = cmd.result()
            except Exception as exc:
                return False
            else:
                return True
        return False

class ServiceDatabase(Service):
    families = (('mysql','MySQL'),('postgres','PostgreSQL'))
    family = models.CharField(max_length=20, choices=families, default='postgres')
    dbname = models.CharField(max_length=50)
    

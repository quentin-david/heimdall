from django.db import models
import json, requests, concurrent.futures

"""
Foreman
"""
class Foreman(models.Model):
    ip = models.GenericIPAddressField()
    protocols = (('http','http'),('https','https'),)
    protocol = models.CharField(max_length=20, choices=protocols, default='https')
    api_user = models.CharField(max_length=30)
    api_user_pwd = models.CharField(max_length=30)
    
    def __str__(self):
        if self.checkApi():
            return self.ip+' (OK)'
        else:
            return self.ip+' (unreachable)'
    
    # Main function to make asynchrone call to Foreman
    # return json or False
    def apiCall(self,resource):
        #json.loads(requests.get("https://192.168.0.11/api/compute_resources",auth=("user_api", "PasswordApi"), verify=False).content.decode())
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            url = self.protocol+'://'+self.ip+'/api/'+resource
            cmd = executor.submit(requests.get, url,auth=(self.api_user, self.api_user_pwd), verify=False)
            try:
                data = cmd.result()
            except Exception as exc:
                return False
            else:
                return data.json()
    
    def checkApi(self):
        return self.apiCall('')
    
    def getHostList(self):
        response = self.apiCall('compute_resources')
        return response
    
    def getNodeListByHost(self,host):
        node_list = self.apiCall('hosts')
        response = []
        if(node_list):
            for node in node_list['results']:
                if(node['compute_resource_name'] == host):
                    response.append(node)
        return response
                
    
    def getNodeByName(self, node_name):
        node_list = self.apiCall('hosts')
        if(node_list):
            for node in node_list['results']:
                if(node['name'] == node_name):
                    return self.getNode(node['id'])
        return False
        
    def getNode(self,node_id):
        node = self.apiCall('hosts/'+str(node_id))
        return node
    
    # VM specs
    def getNodeVmSpecs(self,node_id):
        node_specs = self.apiCall('hosts/'+str(node_id)+'/vm_compute_attributes')
        return node_specs

    def getPuppetClass(self,puppet_class_id):
        puppet_class = self.apiCall('puppetclasses/'+str(puppet_class_id))
        return puppet_class
    
    def getPuppetParameter(self,parameter_id):
        parameter = self.apiCall('smart_class_parameters/'+str(parameter_id))
        return parameter
    
    
    """
    Node creation from Heimdall
    """
    def apiPostCall(self,resource,data):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            url = self.protocol+'://'+self.ip+'/api/'+resource
            cmd = executor.submit(requests.post, url, data, auth=(self.api_user, self.api_user_pwd), verify=False)
            try:
                data = cmd.result()
            except Exception as exc:
                return False
            else:
                return data.json()
            
    def createForemanNodeFromNode(self,node):
        return False


 
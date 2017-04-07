from django.db import models
import requests
import concurrent.futures
#from mapping.models import Node

"""
Munin
"""
class Munin(models.Model):
    ip = models.GenericIPAddressField()
    method = models.CharField(max_length=5)
    server = models.ForeignKey('mapping.Node',on_delete=models.SET_NULL ,blank=True, null=True)
    
    def __str__(self):
        if(self.server):
            return str(self.server.name+' ('+self.ip+')')
        else:
            return str(self.ip)
    
    # Check if munin is responding
    def checkApi(self):
        response = self.apiAsyncCall('')
        return response
    
    # Main function to make asynchrone call to Munin
    # return img or False
    def apiAsyncCall(self,resource):
        #json.loads(requests.get("https://192.168.0.11/api/compute_resources",auth=("user_api", "PasswordApi"), verify=False).content.decode())
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            url = self.method+'://'+str(self.ip)+'/munin/'+resource
            cmd = executor.submit(requests.get, url,verify=False,stream=True)
            try:
                data = cmd.result()
            except Exception as exc:
                return False
            else:
                if data.status_code == '404':
                    return False
                else:
                    return data.raw
                #return data.status_code
                

    
    def getMuninPicture(self,node_name,resource_type,resource_time):
        #response = self.apiAsyncCall('blndgsd01/blndgsd01/diskstats_iops/blndgsd01_vg_lvhome-day.png')
        url = node_name+'/'+node_name+'/'+resource_type+'-'+resource_time+'.png'
        response = self.apiAsyncCall(url)
        return response


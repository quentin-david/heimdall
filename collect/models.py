from django.db import models
from django.contrib.postgres.fields import JSONField
import sys, os
import datetime
import json
from django.utils.timezone import utc
sys.path.insert(0,'/usr/local/bin/collect_scripts')
import collect_download_file as cdf


class CollectItem(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    families = (('file', 'File'),('script', 'Complex script'),('cmd','Sys command'),('stat', 'Stats'),)
    family = models.CharField(max_length=10, choices=families)
    path = models.CharField(max_length=50, null=True,blank=True) #if it's a file
    command = models.CharField(max_length=100, null=True, blank=True) # if it's a system command
    script = models.CharField(max_length=100, null=True, blank=True) #if it's a script to execute
    frequencies = (('hourly','Hourly'),('daily','Daily'),('weekly', 'Weekly'),)
    frequency = models.CharField(max_length=10, choices=frequencies)
    
    def __str__(self):
        if self.path != '':
            return self.path
        elif self.command != '':
            return self.command
        else:
            return self.name
    
class CollectProfile(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    collect_items = models.ManyToManyField(CollectItem, blank=True)
    
    def __str__(self):
        return self.name

"""
class CollectBatch(models.Model):
    date =
    nb_node_collected =
    nb_item_collected =
    nb_error =
    
""" 

class Collect(models.Model):
    node = models.ForeignKey('mapping.Node')
    item = models.ForeignKey(CollectItem)
    date = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField()
    data_file = models.TextField(null=True, blank=True)
    data_json = JSONField(null=True, blank=True)
    
    class Meta:
        get_latest_by = "date"
    
    
    """
    collect all the data for a given node
    """
    def collectNode(self, node):
        last_collect = node.getNodeLastCollect() # to check if the last collect is up to date
        nb_updated = 0
        nb_error = 0
        error_msg = ''
        if not self.checkSSHConnection(node.ip_admin, 'david'):
            return 0,0,0,'node '+node.name+' unreachable !'
        for item in node.collect_profile.collect_items.all():
            if self.isLastItemObsolete(last_collect, item) or last_collect == '':
                nb_updated += 1
                if item.family == 'file':
                    # Download the file
                    data_collected = self.collectDownloadFile(node.ip_admin, 'david', item.path)
                    # save as data_file
                    if data_collected:
                        collect = Collect(node=node,item=item,success=True,data_file=data_collected)
                        collect.save()
                    else:
                        #collect = Collect(node=node,item=item,success=False,data_file=None)
                        error_msg = node.name+" - can't find file : "+item.path
                        nb_error += 1
                elif item.family == 'script':
                    # execute the command
                    data_collected = self.collectExecuteRemoteScript(node.ip_admin, 'david', item.script)
                    if data_collected:
                        # save in data_json
                        data_collected = json.dumps(data_collected)
                        collect = Collect(node=node,item=item,success=True,data_json=data_collected)
                        collect.save()
                    else:
                        #collect = Collect(node=node,item=item,success=False,data_json=None)
                        error_msg = node.name+" - can't find script : "+item.script
                        nb_error += 1
                elif item.family == 'cmd' or item.family == 'stat':
                    # don't know yet
                    pass
        nb_stale = len(node.collect_profile.collect_items.all()) - nb_updated - nb_error
        return nb_updated, nb_stale, nb_error, error_msg
    
    # check if node is reachable with SSH
    def checkSSHConnection(self,ip_addr,user):
        return cdf.checkSSHConnection(ip_addr,user)
    
    # Collect file
    def collectDownloadFile(self,ip_addr,user,filepath):
        return cdf.download(ip_addr, user, filepath)
    
    # Execute remote script
    def collectExecuteRemoteScript(self,ip_addr,user,scriptpath):
        result = cdf.remoteScript(ip_addr, user, scriptpath)
        if result == '':
            return False
        else:
            return result
    
    
    """
    check is the the last collect is up-to-date according to the precision (hourly, daily...) of the item
    """
    def isLastItemObsolete(self, last_node_collect, item):
        for col_item in last_node_collect:
            if col_item.item == item:
                interval = (datetime.datetime.utcnow().replace(tzinfo=utc) - col_item.date)
                if item.frequency == 'hourly':
                    if interval.seconds <= 3600:
                        return False
                elif item.frequency == 'daily':
                    if interval.seconds <= (3600 * 24):
                        return False
                elif item.frequency == 'weekly':
                    if interval.seconds <= (3600 * 24 * 7):
                        return False
                else:
                    return True
        return True
    
    
    """
    get all nodes who are late on their collect
    """
    def getLateCollectNode(self,node_list):
        late_node_list = []
        for node in node_list:
            if node.collect_profile != None:
                last_collect = node.getNodeLastCollect()
                for item in node.collect_profile.collect_items.all():
                    if self.isLastItemObsolete(last_collect,item):
                        late_node_list.append(node)
                        break
        return late_node_list
    
    
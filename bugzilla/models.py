from django.db import models
from django.contrib.auth.models import User
from mapping.models import Application

class Bugzilla(models.Model):
    title = models.CharField(max_length=50,null=False,blank=False,unique=True)
    application = models.ForeignKey(Application,null=True,blank=True)
    owner = models.ForeignKey(User)
    states = (('open','Open'),('close', 'Close'),('info','Info'),)
    state = models.CharField(max_length=15, choices=states, null=False,blank=False)
    date_creation = models.DateTimeField(auto_now=True)
    date_update = models.DateTimeField(auto_now=True)
    content = models.TextField(null=True,blank=True)
    
    class Meta:
        ordering = ['-date_update']

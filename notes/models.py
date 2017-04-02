from django.db import models
from django.contrib.auth.models import User


def file_naming(instance,name):
    return "notes/{}-{}".format(instance.id, name)

class Notes(models.Model):
    title = models.CharField(max_length=50,null=False,blank=False,unique=True)
    owner = models.ForeignKey(User)
    states = (('draft','Draft'),('info','Info'),)
    state = models.CharField(max_length=15, choices=states, null=False,blank=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=True)
    shared = models.BooleanField(default=False)
    category = models.ForeignKey('notes.Category', null=True, on_delete=models.SET_NULL)
    content = models.TextField(null=True,blank=True)
    
    class Meta:
        ordering = ['-date_update']

   
# files attached to the notes  
class NotesFile(models.Model):
    notes = models.ForeignKey('notes.Notes', on_delete=models.CASCADE)
    uploaded_file = models.FileField(upload_to="notes/", null=True,blank=True)
    
    def short_name(self):
        return str(self.uploaded_file).split('/')[-1]
    
     
"""
draft : collection de site
"""
class Bookmark(models.Model):
    url = models.CharField(max_length=300)
    owner = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('notes.Category', blank=True,null=True)
    class Meta:
        ordering = ['-date']


"""
Categories : applied to notes, bookmarks, etc
"""
class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('notes.Category',null=True,blank=True)
    
    class Meta:
        #ordering = ['parent__parent__name']
        ordering = ['name']
        
    # Show the level of imbrication (3 levels max)
    def __str__(self):
        if self.parent:
            if self.parent.parent:
                return self.parent.parent.name+' > '+self.parent.name+' > '+self.name
            else:
                return self.parent.name+' > '+self.name
        else:
            return self.name
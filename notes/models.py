from django.db import models
from django.contrib.auth.models import User
import os.path
from django.db.models import Q
from datetime import datetime
from django.conf import settings
import hashlib
from datetime import datetime


class Notes(models.Model):
    title = models.CharField(max_length=50,null=False,blank=False,unique=True)
    owner = models.ForeignKey(User)
    states = (('draft','Draft'),('info','Info'),)
    state = models.CharField(max_length=15, choices=states, default='draft', null=False, blank=False)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=True)
    shared = models.BooleanField(default=False)
    category = models.ForeignKey('notes.Category', null=True, on_delete=models.CASCADE)
    content = models.TextField(null=True,blank=True)
    
    class Meta:
        ordering = ['-date_update']

    def can_user_see(self, user):
        if self.category.community.owner == user or self.category.parent.community.owner == user: #you're the owner, no problem
            return True
        else:
            return CommunityUsers.objects.filter(community=self.category.community, user=user)

    def can_user_edit(self,user):
        if not CommunityUsers.objects.filter(community=self.category.community, user=user):
            return False
        else:
            if self.can_user_see(user) and CommunityUsers.objects.filter(Q(community=self.category.community) | Q(community=self.category.parent.community), user=user).can_edit == True:
                return True
            else:
                return False


def file_naming(instance,name):
    #return "notes/{}-{}".format(instance.notes.id, name)
    notes_directory = 'notes'
    hasher = hashlib.md5()
    hasher.update(name.encode('utf-8')+str(datetime.now()).encode('utf-8'))
    obfuscated_name = hasher.digest()
    return '{}/{}-{}'.format(notes_directory,instance.notes.id,obfuscated_name)   
   
# files attached to the notes  
class NotesFile(models.Model):
    notes = models.ForeignKey('notes.Notes', on_delete=models.CASCADE)
    original_name = models.CharField(max_length=150)
    uploaded_file = models.FileField(upload_to=file_naming,null=True,blank=True) #hashed name
    
    def short_name(self):
        return str(self.uploaded_file).split('/')[-1]
    
    def delete_physical_file(self):
        file_path = settings.MEDIA_ROOT+self.uploaded_file.name
        if os.path.exists(file_path):
            return os.unlink(file_path)
        else:
            return True
    
    def is_present(self):
        if os.path.exists(settings.MEDIA_ROOT+self.uploaded_file.name):
            return True
        else:
            return False
     
"""
Bookmark : collection de site
"""
class Bookmark(models.Model):
    url = models.CharField(max_length=300)
    #owner = models.ForeignKey(User)
    date = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('notes.Category', blank=True,null=True, on_delete=models.CASCADE)
    class Meta:
        ordering = ['-date']

    def get_bookmarks_by_user(user):
        return self.objects.filter(category__in = Category.get_subcategories_by_user(user))
"""
Categories : applied to notes, bookmarks, etc
"""
class Category(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey('notes.Category',null=True,blank=True, on_delete=models.CASCADE)
    community = models.ForeignKey('notes.Community', blank=True, null=True)
    
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
    
    # Check if the user is in the right community to see that category and its items
    def can_user_see(self, user):
        if self.community.owner == user or self.parent.community.owner == user: #you're the owner, no problem
            return True
        else:
            if CommunityUsers.objects.filter(Q(community=self.community) | Q(community=self.parent.community), user=user):
                return True
            else:
                return False
     
    # List all subcategories (level 2 and 3) accessible by the user
    # Check if
    #   - the user own the community
    #   - OR is part of the community AND has enabled it
    def get_subcategories_by_user(user):
        #return Category.objects.filter(Q(community__owner=user) | (Q(community__communityusers__user=user) & Q(community__communityusers__user_visa=True)) | (Q(parent__community__communityusers__user=user) & Q(parent__community__communityusers__user_visa=True)), parent__isnull=False).distinct()
        return Category.objects.filter(Q(community__in = Community.get_communities_by_user(user)))
        
    def get_root_categories_by_user(user):
        #return Category.objects.filter(Q(community__owner=user) | (Q(community__communityusers__user=user) & Q(community__communityusers__user_visa=True)), parent__isnull=True).distinct()
        return Category.objects.filter(Q(community__in = Community.get_communities_by_user(user), parent__isnull=True))
    
    # Active categories
    def get_categories_by_user(user):
        #return Category.objects.filter(Q(community__owner=user) | (Q(community__communityusers__user=user) & Q(community__communityusers__user_visa=True))).distinct()
        return Category.objects.filter(Q(community__in = Community.get_communities_by_user(user)))
    
    # All categories
    def get_all_categories_by_user(user):
        return Category.objects.filter(Q(community__in = Community.get_all_communities_by_user(user)))
    
    # Return the total number of bookmark attached to a category and all of its subcategories
    def get_nb_total_bookmark(self):
        nb_total = 0
        nb_total += len(self.bookmark_set.all())
        for kid in self.category_set.all():
            nb_total += len(kid.bookmark_set.all())
        return nb_total
    
    # Return the total number of notes attached to a category and all of its subcategories
    def get_nb_total_notes(self):
        nb_total = 0
        nb_total += len(self.notes_set.all())
        for kid in self.category_set.all():
            nb_total += len(kid.notes_set.all())
        return nb_total
    
    def get_file_list(self):
        return NotesFile.objects.filter(notes__in=self.notes_set.all())
    
"""
Community
"""
class Community(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    community_users = models.ManyToManyField(User, blank=True, through='CommunityUsers', related_name='contributors')

    def __str__(self):
        return self.name+' ('+self.owner.username+')'
    
    # Get root categories for a community
    def get_root_categories_by_community(self):
        return self.category_set.filter(parent__isnull=True)
    
    # List all communities activated by the user
    # Check if
    #   - the user own the community
    #   - OR is part of the community AND has enabled it
    def get_communities_by_user(user):
        #return Community.objects.filter((Q(community_users=user) & Q(communityusers__user_visa=True)) | (Q(owner=user) & Q(communityusers__user_visa=True) )).distinct()
        return Community.objects.filter((Q(community_users=user) & Q(communityusers__user_visa=True))).distinct()

    # List all communities the user can activate
    def get_all_communities_by_user(user):
        return Community.objects.filter(Q(communityusers__in=CommunityUsers.get_all_communities_by_user(user))).distinct()
    
    def is_shared(self):
        if self.community_users.count() > 1:
            return True
        else:
            return False
        
    def get_contributors(self):
        user_list = []
        for user in self.community_users.distinct():
            if user != self.owner:
                user_list.append(user)
        return user_list
    
    
class CommunityUsers(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    can_add = models.BooleanField(default=True)
    can_edit = models.BooleanField(default=False)
    user_visa = models.BooleanField(default=True) # Set if the user accept this community or not
    
    def get_all_communities_by_user(user):
        return CommunityUsers.objects.filter(Q(user=user)).distinct()
    
        
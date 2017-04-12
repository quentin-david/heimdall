from django import forms
from .models import Notes, Category, Bookmark, Community, CommunityUsers
from django.db.models import Q
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Button
from crispy_forms.bootstrap import InlineField
from crispy_forms.bootstrap import FormActions
import re

"""
Notes
"""
class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        exclude = ['owner','category']
    

"""
Categories have 3 level of imbrication
"""
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CategoryForm,self).__init__(*args, **kwargs)
        # Only display first and second level of imbrication
        # TODO : A user can't add a sub-category to a shared category
        if self.user:
            self.fields["parent"].queryset = Category.objects.filter((Q(parent__isnull=True) | Q(parent__parent__isnull=True)) & Q(community__owner=self.user)).distinct()
            #self.fields["community"].queryset = Community.objects.filter((Q(community_users=self.user) & Q(communityusers__user_visa=True)) | Q(owner=self.user)).distinct()
            self.fields["community"].queryset = Community.get_communities_by_user(self.user)
        
        
class BookmarkForm(forms.ModelForm):
    class Meta:
        model = Bookmark
        fields = ('url', 'category')
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(BookmarkForm,self).__init__(*args,**kwargs)
        # Only display second and third level of imbrication
        if self.user:
            # TODO : if it's an external community, check if the user can_add
            #self.fields["category"].queryset = Category.objects.filter(Q(community__owner=self.user) | (Q(community__communityusers__user=self.user) & Q(community__communityusers__user_visa=True)) | (Q(parent__community__communityusers__user=self.user) & Q(parent__community__communityusers__user_visa=True)), parent__isnull=False).distinct()
            self.fields["category"].queryset = Category.get_subcategories_by_user(self.user)
        
    def clean_url(self):
        url = self.cleaned_data['url']
        if not re.match('http', url):
            return 'http://'+url
        else:
            return url

"""
Community
"""
class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        exclude = ['owner']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(CommunityForm,self).__init__(*args,**kwargs) 
    
    def clean_name(self):
        name = self.cleaned_data['name']
        if re.match('^perso', name):
            if name == 'perso'+self.user.username:
                return name
            else:
                raise forms.ValidationError("Community named perso-* are reserved")
        else:
            return name

class CommunityUsersForm(forms.ModelForm):
    class Meta:
        model = CommunityUsers
        exclude = ['community','user_visa']
        
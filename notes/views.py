from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from .models import Notes, Category, Bookmark, NotesFile, Community, CommunityUsers
from .forms import NotesForm, CategoryForm, BookmarkForm, CommunityForm, CommunityUsersForm
from django.views.decorators.csrf import csrf_exempt
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.db.models import Q
from django.forms import modelformset_factory

"""
Notes
"""

def notesList(request):
    #communities = Community.objects.filter((Q(community_users=request.user) & Q(communityusers__user_visa=True)) | Q(owner=request.user)).distinct()
    community_list = Community.get_communities_by_user(request.user)
    # TODO : check if user_visa == True
    #notes_list = Notes.objects.filter(Q(category__community__communityusers__user=request.user) | Q(category__community__owner=request.user), category__community__communityusers__user_visa = True).distinct()
    notes_list = Notes.objects.filter((Q(category__community__communityusers__user=request.user) & Q(category__community__communityusers__user_visa = True))| Q(category__community__owner=request.user)).distinct()
    return render(request, 'notes/notes_list.html', locals())



def notesCreateOrUpdate(request, category_id, notes_id=None):
    #root_category_list = Category.objects.filter(parent__isnull=True)
    community_list = Community.get_communities_by_user(request.user)
    category = Category.objects.get(id=category_id)
    if notes_id:
        note_to_edit = Notes.objects.get(id=notes_id)
        # Check if the user has the rights to edit that note
        if not note_to_edit.can_user_see(request.user):
            messages.info(request, 'You dont have the rights to edit that note')
            return redirect('notes_list')
        upfiles = note_to_edit.notesfile_set.all()
    else:
        note_to_edit = None
    form = NotesForm(request.POST or None,request.FILES or None, instance=note_to_edit)
    files = request.FILES.getlist('uploaded_files')
    if form.is_valid():
        note = form.save(commit=False)
        note.owner = request.user
        note.category = category
        note.save()
        for upfile in files:
            f = NotesFile(notes=note, uploaded_file=upfile)
            f.save()
        return redirect('topic_view', category_id=note.category.id)
    return render(request,'notes/notes_create_form.html',locals())



def notesDelete(request, notes_id):
    notes_to_delete = Notes.objects.get(id=notes_id)
    community_list = Community.get_communities_by_user(request.user)
    if request.method == 'POST':
        # Deletion of all the physical files
        for notes_file in NotesFile.objects.filter(notes=notes_to_delete):
            notes_file.delete_physical_file()
        notes_to_delete.delete()
        messages.success(request, 'Notes "{}" deleted !'.format(notes_to_delete.title))
        return redirect('topic_view', category_id=notes_to_delete.category.id)
    return render(request, 'notes/notes_delete.html', locals())


"""
NotesFile
"""
# Ajax call (csrf disabled...probably not the right thing to do)
@csrf_exempt
def notesFileDelete(request, notes_file_id):
    file_to_delete = NotesFile.objects.get(id=notes_file_id)
    if file_to_delete:
        file_to_delete.delete_physical_file()
        file_to_delete.delete()
    messages.success(request, 'File "{}" deleted !'.format(file_to_delete.uploaded_file))
    return redirect('topic_view', category_id=file_to_delete.notes.category.id)


"""
Categories
"""
def categoryList(request, category_id=None):
    community_list = Community.get_communities_by_user(request.user)
    personal_communities = Community.objects.filter(owner=request.user)
    shared_communities = CommunityUsers.objects.filter(user=request.user)
    if category_id:
        category_to_edit = Category.objects.get(id=category_id)
    else:
        category_to_edit = None
    form = CategoryForm(None, instance=category_to_edit, user=request.user)
    return render(request, 'category/category_list.html', locals())


def categoryCreateOrUpdate(request, category_id=None):
    if category_id:
        category_to_edit = Category.objects.get(id=category_id)
    else:
        category_to_edit = None
    form = CategoryForm(request.POST, instance=category_to_edit)
    if form.is_valid():
        category = form.save(commit=False)
        # Sub categories have the same community as their parents
        if category.parent:
            category.community = Category.objects.get(name=category.parent).community
        else:
            # if no community is given, the default is the personal community (perso-*)
            if category.community == None:
                category.community = Community.objects.get(name='perso-'+request.user.username)
        category.save()
        return redirect('category_list')
    return render(request, 'category/category_list.html', locals())


class CategoryDelete(DeleteView):
    model = Category
    context_object_name = 'category'
    template_name = 'category/category_delete.html'
    success_url = reverse_lazy('category_list')
    def get_context_data(self, **kwargs):
        context = super(CategoryDelete, self).get_context_data(**kwargs)
        context['community_list'] = Community.get_communities_by_user(self.request.user)
        return context

"""
Bookmark
"""
def bookmarkCreate(request):
    form = BookmarkForm(request.POST or None)
    if form.is_valid():
        bookmark = form.save(commit=False)
        bookmark.owner = request.user
        bookmark.save()
        return redirect('topic_view', category_id=bookmark.category.id)
    return render(request, 'bookmark/bookmark_list.html', locals())


def bookmarkList(request):
    unsorted_bookmark_list = Bookmark.objects.filter(category__isnull=True)
    #communities = Community.objects.filter((Q(community_users=request.user) & Q(communityusers__user_visa=True)) | Q(owner=request.user)).distinct()
    community_list = Community.get_communities_by_user(request.user)
    bookmark_form = BookmarkForm(None)

    return render(request, 'bookmark/bookmark_list.html', locals())


def bookmarkDelete(request, bookmark_id):
    bookmark_to_delete = Bookmark.objects.get(id=bookmark_id)
    if bookmark_to_delete:   
        bookmark_to_delete.delete()
    messages.success(request, 'Bookmark "{}" deleted !'.format(bookmark_to_delete.url))
    return redirect('topic_view', category_id=bookmark_to_delete.category.id)

"""
Topic
list every elements (Notes, bookmarks...) by category
"""
def topicView(request, category_id):
    category = Category.objects.get(id=category_id)
    if not category.can_user_see(request.user):
        messages.info(request, 'You dont have the rights to see that category')
        return redirect('notes_list')
    
    community_list = Community.get_communities_by_user(request.user)
    bookmark_list = Bookmark.objects.filter(category=category.id)
    bookmark_form = BookmarkForm(None, user=request.user, initial={'category':category.id})
    #form = NotesForm(None, user=request.user, initial={'category':category.id})
    form = NotesForm(None)
    notes_list = Notes.objects.filter(category=category)
    
    return render(request, 'topic/topic_view.html', locals())


"""
Community
"""
def communityCreateOrUpdate(request, community_id=None):
    CommunityUsersFormFormset = modelformset_factory(CommunityUsers, form=CommunityUsersForm, exclude=('community',), extra=1)    
    if community_id:
        community_to_edit = Community.objects.get(id=community_id)
        community_users_form = CommunityUsersFormFormset(request.POST or None, queryset=CommunityUsers.objects.filter(community=community_to_edit))
    else:
        community_to_edit = None
        community_users_form = CommunityUsersFormFormset(request.POST or None, queryset=CommunityUsers.objects.none())
    form = CommunityForm(request.POST or None, user=request.user, instance=community_to_edit)
    
    if form.is_valid():
        community = form.save(commit=False)
        community.owner = request.user
        CommunityUsers.objects.filter(community=community).delete() # Delete every contributors before adding new (probably not the right way...)
        community.save()
        if community_users_form.is_valid():
            for user in community_users_form:
                u = user.save(commit=False)
                u.community = community
                u.save()

        return redirect('profile')
    return render(request, 'community/community_create_form.html', locals())


# Ajax call (csrf disabled...probably not the right thing to do)
# enable/disable visa on external community
@csrf_exempt
def sharedCommunityToggle(request, shared_community_id):
    shared_community = CommunityUsers.objects.get(user=request.user, community=shared_community_id)
    if shared_community.user_visa == True:
        shared_community.user_visa = False
    else:
        shared_community.user_visa = True
    shared_community.save()
    
    return redirect('profile')


# Delete whole community
# Categori and notes aren't delete, they are moved to the user's personal community
def communityDelete(request, community_id):
    community_list = Community.get_communities_by_user(request.user)
    community_to_delete = Community.objects.get(id=community_id)
    personal_community = Community.objects.get(name='perso-'+request.user.username)
    if request.method == 'POST':
        # Check if the user has a personal community
        if personal_community:
            categories_to_move = community_to_delete.category_set.all()
            for category in categories_to_move:
                category.community = personal_community
                category.save()
                messages.success(request, 'Category : '+category.name+' has been moved')
            community_to_delete.delete()   
            messages.success(request, 'Community : '+community_to_delete.title+' has been deleted')
        else:
            messages.danger(request, 'You dont have a personal community')
        return redirect('profile')
    return render(request, 'community/community_delete.html', locals())


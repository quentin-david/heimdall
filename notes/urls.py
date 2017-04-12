from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    # Notes
    #url(r'^$', login_required(views.NotesList.as_view()), name='notes_list'),
    url(r'^$', login_required(views.notesList), name='notes_list'),
    url(r'^(?P<category_id>\d+)/new/$', login_required(views.notesCreateOrUpdate), name='notes_create'),
    url(r'^(?P<category_id>\d+)/(?P<notes_id>\d+)/edit$', login_required(views.notesCreateOrUpdate), name='notes_update'),
    url(r'^(?P<notes_id>\d+)/delete$', login_required(views.notesDelete), name='notes_delete'),
    # NotesFile
    url(r'^file/(?P<notes_file_id>\d+)/delete', login_required(views.notesFileDelete), name='notes_file_delete'),
    # Categories
    url(r'^category$', login_required(views.categoryList), name='category_list'),
    url(r'^category/new/$', login_required(views.categoryCreateOrUpdate), name='category_create'),
    url(r'^category/edit/(?P<category_id>\d+)$', login_required(views.categoryCreateOrUpdate), name='category_update2'),
    url(r'^category/(?P<category_id>\d+)/edit$', login_required(views.categoryList), name='category_update'),
    #url(r'^category/(?P<category_id>\d+)/edit$', login_required(views.categoryCreateOrUpdate), name='category_update'),
    url(r'^category/(?P<pk>\d+)/delete$', login_required(views.CategoryDelete.as_view()), name='category_delete'),
    # Bookmarks
    url(r'^bookmark$', login_required(views.bookmarkList), name='bookmark_list'),
    url(r'^bookmark/new/$', login_required(views.bookmarkCreate), name='bookmark_create'),
    url(r'^bookmark/(?P<bookmark_id>\d+)/delete$', login_required(views.bookmarkDelete), name='bookmark_delete'),
    # Topic
    url(r'^topic/(?P<category_id>\d+)/view$', login_required(views.topicView), name='topic_view'),
    # Community
    url(r'^community/new/$', login_required(views.communityCreateOrUpdate), name='community_create'),
    url(r'^community/(?P<community_id>\d+)/edit$', login_required(views.communityCreateOrUpdate), name='community_update'),
    url(r'community/(?P<shared_community_id>\d+)/toggle$', login_required(views.sharedCommunityToggle), name='community_toggle_community'),
    url(r'^community/(?P<community_id>\d+)/delete$', login_required(views.communityDelete), name='community_delete'),
]
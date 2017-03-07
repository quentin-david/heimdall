from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from .models import Exercice

urlpatterns = [
    url(r'home$' , login_required(views.exerciceHome), name='exercice_home'),
    url(r'exercice/new$', login_required(views.ExerciceCreate.as_view()), name='exercice_create'),
    url(r'exercice/edit/(?P<pk>\d+)$', login_required(views.ExerciceUpdate.as_view()), name='exercice_update'),
    url(r'exercice/delete/(?P<pk>\d+)$', login_required(views.ExerciceDelete.as_view()), name='exercice_delete'),
    url(r'graph$', views.graph, name='exercice_graph'),
]
from django.shortcuts import render
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Foreman
from .forms import ForemanForm

class ForemanList(ListView):
    model = Foreman
    context_object_name = 'foreman_list'
    template_name = 'foreman/foreman_list.html'

class ForemanCreate(CreateView):
    model = Foreman
    form_class = ForemanForm
    template_name = 'foreman/foreman_create_form.html'
    success_url = reverse_lazy('foreman_list')

class ForemanUpdate(UpdateView):
    model = Foreman
    form_class = ForemanForm
    template_name = 'foreman/foreman_create_form.html'
    success_url = reverse_lazy('foreman_list')
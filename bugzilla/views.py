from django.shortcuts import render, redirect
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from django.db.models import Q
from .models import Bugzilla
import operator
from functools import reduce
from .forms import BugzillaForm, BugzillaSearchForm

"""
class BugzillaList(ListView):
    model = Bugzilla
    context_object_name = 'bugzilla_list'
    template_name = 'bugzilla/bugzilla_list.html'
    def get_context_data(self, **kwargs):
        context = super(BugzillaList, self).get_context_data(**kwargs)
        context['search_form'] = BugzillaSearchForm()
        return context
"""

class BugzillaSearchList(ListView):
    queryset = Bugzilla.objects.all()
    context_object_name = 'bugzilla_list'
    template_name = 'bugzilla/bugzilla_list.html'
    
    def get_queryset(self):
        qs = super(BugzillaSearchList,self).get_queryset()
        qs_owner = self.request.GET.get('qs_owner')
        qs_title = self.request.GET.get('qs_title')
        qs_state = self.request.GET.get('qs_state')
        qs_application = self.request.GET.get('qs_application')
        
        conditions = []
        if qs_state != '' and qs_state is not None:
            conditions.append(('state',qs_state))
        if qs_owner != '' and qs_owner is not None:
            conditions.append(('owner', qs_owner))
        if qs_application != '' and qs_application is not None:
            conditions.append(('application', qs_application))
        if qs_title != '' and qs_title is not None:
            conditions.append(('title__contains', qs_title))
        
        if len(conditions) > 0:
            q_filters = [Q(x) for x in conditions]
            qs = qs.filter(reduce(operator.and_,q_filters))
        else:
            qs = Bugzilla.objects.all()
           
        return qs
    
    def get_context_data(self, **kwargs):
        context = super(BugzillaSearchList, self).get_context_data(**kwargs)
        context['search_form'] = BugzillaSearchForm(context)
        context['qs_title'] = self.request.GET.get('qs_title')
        context['qs_state'] = self.request.GET.get('qs_state')
        context['qs_owner'] = self.request.GET.get('qs_owner')
        context['qs_application'] = self.request.GET.get('qs_application')
        return context
        


def bugzillaCreate(request, application_id=None):
    if application_id:
        appli = Application.objects.get(id=application_id)
    form = BugzillaForm(request.POST or None)
    if form.is_valid():
        bug = form.save(commit=False)
        bug.owner = request.user
        bug.save()
        return redirect('bugzilla_list')
    return render(request,'bugzilla/bugzilla_create_form.html',locals())

class BugzillaUpdate(UpdateView):
    model = Bugzilla
    form_class = BugzillaForm
    template_name = 'bugzilla/bugzilla_create_form.html'
    success_url = reverse_lazy('bugzilla_list')

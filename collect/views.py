from django.shortcuts import render, redirect
#from django.db.models import Max
from django.contrib import messages
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView, FormView
from django.core.urlresolvers import reverse_lazy
from .models import CollectProfile, CollectItem, Collect
from .forms import CollectProfileForm, CollectItemForm
from mapping.models import Node


def collectHome(request):
    collect_profile_list = CollectProfile.objects.all()
    collect_item_list = CollectItem.objects.all()
    collect_history = Collect.objects.order_by('-date')
    node_list = Node.objects.filter(is_collected=True)
    collect_late_node = Collect().getLateCollectNode(node_list)
    return render(request, 'collect/collect_home.html', locals())

"""
Profile
"""
class CollectProfileCreate(CreateView):
    model = CollectProfile
    form_class = CollectProfileForm
    template_name = 'profile/collect_profile_create_form.html'
    success_url = reverse_lazy('collect_home')

class CollectProfileUpdate(UpdateView):
    model = CollectProfile
    form_class = CollectProfileForm
    template_name = 'profile/collect_profile_create_form.html'
    success_url = reverse_lazy('collect_home')

class CollectProfileDelete(DeleteView):
    model = CollectProfile
    context_object_name = 'profile'
    template_name = 'profile/collect_profile_delete.html'
    success_url = reverse_lazy('collect_home')


"""
Items
"""
class CollectItemCreate(CreateView):
    model = CollectItem
    form_class = CollectItemForm
    template_name = 'profile/collect_item_create_form.html'
    success_url = reverse_lazy('collect_home')

class CollectItemUpdate(UpdateView):
    model = CollectItem
    form_class = CollectItemForm
    template_name = 'profile/collect_item_create_form.html'
    success_url = reverse_lazy('collect_home')    
    
"""
Collect a node
"""
def collectNode(request,node_id):
    node = Node.objects.get(id=node_id)
    nb_updated, nb_stale, nb_error, error_msg = Collect().collectNode(node)
    if error_msg:
        messages.warning(request, error_msg)
    else:
        messages.success(request, 'Collect OK for {} - {} element collected - {} already up-to-date'.format(node.name,nb_updated, nb_stale))
    
    return redirect('node_collect', node_id=node_id)

"""
collect every nodes
"""
def collectEveryNode(request):
    nb_node_collected = 0
    nb_element_collected = 0
    nb_element_error = 0
    for node in Node.objects.all():
        if node.collect_profile:
            nb_updated, nb_stale, nb_error, error_msg = Collect().collectNode(node)
            nb_node_collected += 1
            nb_element_error += 1
            nb_element_collected += nb_updated
            if error_msg:
                messages.warning(request, error_msg)
    messages.success(request, 'Global collect OK - {} node collected - {} item updated - {} in error'.format(nb_node_collected, nb_element_collected, nb_element_error))
    
    return redirect('collect_home')



"""
Show collected elements by node
"""
def collectedElementsByNode(request, node_id):
    node = Node.objects.get(id=node_id)
    collect_list = Collect.objects.filter(node=node).order_by('-date')
    file_list = node.getNodeLastCollect()
    return render(request,'collect/collect_node.html', locals())

"""
Purge all collects
"""
def purgeCollect(request):
    Collect.objects.all().delete()
    return redirect('collect_home')

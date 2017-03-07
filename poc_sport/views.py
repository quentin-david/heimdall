from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView,CreateView,DetailView,UpdateView,DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import Exercice
from .forms import ExerciceForm

import pandas as pd
import numpy as np
from pandas import DataFrame
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

def exerciceHome(request):
    exercice_list = Exercice.objects.all()
    liste_dates = Exercice.objects.values_list('date', flat=True)
    liste_valeurs = Exercice.get_list_values()
    return render(request, 'exercice/home.html', locals())

class ExerciceCreate(CreateView):
    model = Exercice
    form_class = ExerciceForm
    template_name = 'exercice/exercice_create_form.html'
    success_url = reverse_lazy('exercice_home')
    
    def get_context_data(self, **kwargs):
        context = super(ExerciceCreate, self).get_context_data(**kwargs)
        context['last_stat'] = Exercice.objects.all()[0]
        return context

class ExerciceUpdate(UpdateView):
    model = Exercice
    form_class = ExerciceForm
    template_name = 'exercice/exercice_create_form.html'
    success_url = reverse_lazy('exercice_home')

class ExerciceDelete(DeleteView):
    model = Exercice
    form_class = ExerciceForm
    template_name = 'exercice/exercice_delete.html'
    success_url = reverse_lazy('exercice_home')



def graph(request):
    #exercice_type_list = ['D (ventre)', 'Q (ventre)', 'D (cote-gauche)', 'Q (cote-gauche)']
    exercice_type_list = ['Deborah','Quentin']
    liste_dates = Exercice.objects.values_list('date', flat=True)
    liste_values = np.array(Exercice.get_list_values()) / 60
    
    
    fig = Figure()
    ax = fig.add_subplot(111)
    #data_df = pd.DataFrame(Exercice.get_list_values(), index=pd.date_range(liste_dates[0], periods=len(liste_dates)), columns=exercice_type_list)
    data_df = pd.DataFrame(liste_values, index=pd.date_range(liste_dates[0], periods=len(liste_values)), columns=exercice_type_list)
    data_df.plot(ax=ax, marker='o')
    canvas = FigureCanvas(fig)
    response = HttpResponse( content_type = 'image/png')
    canvas.print_png(response)
    return response


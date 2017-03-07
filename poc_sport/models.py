from django.db import models
import datetime
from django.contrib.auth.models import User

import numpy as np

class Exercice(models.Model):
    date = models.DateField(default=datetime.date.today)
    exercices = (('ventre','Ventre'),('cote_gauche','cote gauche'),('cote_droit','cote droit'),)
    exercice = models.CharField(max_length=20,choices=exercices)
    temps_qt = models.DurationField(null=True, blank=True)
    temps_db = models.DurationField(null=True, blank=True)
    
    class Meta:
        ordering = ['date']        
    
    def get_temps_total_by_date(self):
        temps_qt = 0
        temps_db = 0
        for exercice in Exercice.objects.filter(date=self.date):
            temps_qt += exercice.temps_qt
            temps_db += exercice.temps.db
        return {'qt': temps_qt, 'db':temps_db}
    
    def get_list_values():
        tableau = []
        for jour in Exercice.objects.values_list('date', flat=True).distinct():
            qt_total=0
            db_total=0
            for exercice in Exercice.objects.filter(date=jour):
                qt_total += exercice.temps_qt.total_seconds()
                db_total += exercice.temps_db.total_seconds()
            tableau.append([db_total, qt_total])
                    
        return tableau

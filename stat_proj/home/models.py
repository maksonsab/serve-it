from pyexpat import model
from django.db import models
from django.forms import IntegerField

# Create your models here.


class EffectModel(models.Model):
    
    class Meta:
        db_table = 'effekt'

    id = models.IntegerField(primary_key=True)
    Period = models.DateField()
    Otdel = models.CharField(max_length=45)
    SredniyChek = models.FloatField()
    KolVoKlientov = models.IntegerField()
    Viruchka = models.FloatField()
    KolVoSotrudnikovOtdela = models.FloatField()
    KolVoSotrudnikovKo = models.FloatField()
    Effekt = models.FloatField()
from django.db import models


class EffectModel(models.Model):
    
    class Meta:
        db_table = 'effekt'
        default_permissions = 'view'
        managed = False

    id = models.IntegerField(primary_key=True)
    Period = models.DateField()
    Otdel = models.CharField(max_length=45)
    SredniyChek = models.FloatField()
    KolVoKlientov = models.IntegerField()
    Viruchka = models.FloatField()
    KolVoSotrudnikovOtdela = models.FloatField()
    KolVoSotrudnikovKo = models.FloatField()
    Effekt = models.FloatField()
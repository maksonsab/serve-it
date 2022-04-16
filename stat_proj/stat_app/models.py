from django.db import models


class ZagruzkaModel(models.Model):
    
    class Meta:
        db_table = 'stp_zagruzka'
        default_permissions = 'view'
        managed = False 

    ID = models.IntegerField(primary_key=True)
    Period = models.DateField()
    Sotrudnik = models.CharField(max_length=45)
    RabVremTabel = models.FloatField()
    RabVremNaryad = models.FloatField()
    ProcentZagr = models.FloatField()
from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse

from . import models

departments = {
    '1c' : '1С',
    'stp' : 'СТП',
    'asutp' : 'АСУ ТП'}


def index(request):
    
    data = []
    for department in departments.values():
        data.append(models.EffectModel.objects.using('data').filter(Otdel = department).order_by('-id')[0:2].all())
    return render(request, 'home/index.html', context={'title' : 'Главная', 'data' : data, 'departments' : departments})

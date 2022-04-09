from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse

from . import models

departments = {
    "1С" : '1c', 
    "СТП": 'stp',
    "АСУ ТП" : 'asutp'}


def index(request):
    
    data = []
    for department in departments:
        data.append(models.EffectModel.objects.using('data').filter(Otdel = department).order_by('-id')[0:2].all())
    '''sql = 'SELECT * FROM effekt WHERE Otdel = "СТП";'
    with connections['data'].cursor() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()'''
    return render(request, 'home/index.html', context={'title' : 'Главная', 'data' : data, 'departments' : departments})

def by_department(request, otdel):
    return HttpResponse('HAHA')
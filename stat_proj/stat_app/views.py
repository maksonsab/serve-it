from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse
from home.models import EffectModel

# Create your views here.

departments = {
    '1c' : '1С',
    'stp' : 'СТП',
    'asutp' : 'АСУ ТП'
}

def index(request):
    return render(request, 'stat_app/index.html')


def by_department(request, department):
    dept = departments.get(department)
    if not dept:
       return HttpResponseNotFound('Такого отдела нет!')
    else:
        data = EffectModel.objects.using('data').filter(Otdel = dept).all()
        month = []
        clients = []
        sc = []
        revenue = []
        employees = []
        profit = []

        for mod in data:
            month.append(mod.Period.strftime('%d-%m-%Y'))
            clients.append(mod.KolVoKlientov)
            sc.append(mod.SredniyChek)
            revenue.append(mod.Viruchka)
            employees.append(mod.KolVoSotrudnikovOtdela)
            profit.append(mod.Effekt)
        print(clients)
        return render(request, 
        'stat_app/department_stat.html', 
        context = {'months' : month, 
        'clients': clients,
        'sc' : sc, 
        'profit' : profit,
        'revenue': revenue,
        'employees' : employees,
        'department' : departments.get(department),
        'departments' : departments})
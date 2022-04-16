from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse

from home.models import EffectModel
from .logic import simple_graph

# Create your views here.

departments = {
    '1c' : '1С',
    'stp' : 'СТП',
    'asutp' : 'АСУ ТП'
}

employees = {
    'Сабирзанов' : 'Сабирзанов Максим',
    'Карянов' : 'Карянов Максим',
    'Соколовский' : 'Соколовский Вячеслав'}

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


def by_employee(request, department: str, employee:str):
    employee_name = employees.get(employee)
    if not employee_name:
        return HttpResponseNotFound('Такого сотрудника нет!')
    context = {
        'department' : departments.get(department), 
        'employee' : employee_name,
        'departments' : departments,
        }
    
    return render(request, 'stat_app/employee_copy.html', context=context)



def data_for_graph(request) -> JsonResponse:
    if request.method == 'POST':
        try:
            year, month = int(request.POST.get('year')), int(request.POST.get('month'))
        except Exception:
            return HttpResponseNotFound('Неверные данные!')
        employee = request.POST.get('employee')
        if not employees.keys():
            return HttpResponseNotFound('Такого сотрудника нет!')
        response_var = simple_graph(employee, year, month)
        response_var['employee'] = employee
        return JsonResponse(response_var)
    else:
        return HttpResponseNotFound('Страница не найдена')
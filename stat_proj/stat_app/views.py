from urllib import response
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, JsonResponse

from home.models import EffectModel
from .logic import simple_graph, zagruzka_graph

# Create your views here.

departments = {
    '1c' : '1С',
    'stp' : 'СТП',
    'asutp' : 'АСУ ТП'
}

employees = {
    'Сабирзанов' : 'Сабирзанов Максим',
    'Карянов' : 'Карянов Максим',
    'Соколовский' : 'Соколовский Вячеслав',
    'Качанов' : "Качанов Леонид",
    "Шевкунова" : "Шевкунова Евгения Викторовна",
    "Мурзинцева" : "Мурзинцева Ксения", 
    "Самойлов" : "Самойлов Алексей",
    "Трегубова" : 'Трегубова Маргарита Владимировна',
    }

def index(request) -> render:
    return render(request, 'stat_app/index.html')

#!!!!переделать!!!!!
def by_department(request, department:str) -> render:
    '''Вьюшка страницы эффективности отдела'''
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
        context = {
            'months' : month, 
            'clients': clients,
            'sc' : sc, 
            'profit' : profit,
            'revenue': revenue,
            'employees' : employees,
            'department' : departments.get(department),
            'departments' : departments,
            'title' : f'Отдел {departments.get(department)}',
        }
        return render(request,'stat_app/department_stat.html', context = context)


def by_employee(request, department: str, employee:str) -> render:
    '''Вьюшка страницы загрузки отдельного сотрудника'''
    employee_name = employees.get(employee)
    if not employee_name:
        return HttpResponseNotFound('Такого сотрудника нет!')
    context = {
        'department' : department,
        'department_ru' : departments.get(department), 
        'employee' : employee_name,
        'departments' : departments,
        'employees' : employees,
        'title' : f'Статистика: {employee_name}'
        }
    return render(request, 'stat_app/employee.html', context=context)


def all_employee(request, department: str) -> render:
    '''Вьюшка страницы загрузки отдела'''
    if department != 'stp':
        return HttpResponseNotFound(f'Информации по отделау {departments.get(department)} ещё нет!')
    context = {
        'departments' : departments,
        'department' : department,
        'department_ru' : departments.get(department),
        'employees' : employees,
        'title' : f'Загруженность {departments.get(department)}'
    }
    return render(request, 'stat_app/employee_all.html', context=context)



def data_for_graph(request) -> JsonResponse:
    '''Этот вью предоставляет данные для графика загрузки конкретного сотрудника'''
    if request.method == 'POST':
        try:
            year, month = int(request.POST.get('year')), int(request.POST.get('month'))
        except Exception:
            return HttpResponseNotFound('Неверные данные!')
        employee = request.POST.get('employee')
        if not employees.keys():
            return HttpResponseNotFound('Такого сотрудника нет!')
        response_var = simple_graph(employee, year, month)
        return JsonResponse(response_var)
    else:
        return HttpResponseNotFound('Страница не найдена')

def zagruzka_view(request) -> JsonResponse:
    '''Этот вью предоставляет данные для графика загрузки отдела'''
    if request.method == 'POST':
        try:
            year, month = int(request.POST.get('year')), int(request.POST.get('month'))
        except Exception:
            return HttpResponseNotFound('Неверные данные!')
        return JsonResponse(zagruzka_graph(year, month))
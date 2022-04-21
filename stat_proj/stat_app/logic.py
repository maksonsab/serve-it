from datetime import date, timedelta
import json
import pickle

from numpy import rec

from .models import ZagruzkaModel

months = ['Январь', 'Февраль', 'Март', "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
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

def generate_month(year:int, month:int) -> list:
    "Возвращает list() с датами в заданном месяце datetime.date"
    december = False

    if month in range(1,13):
        start = date(year, month, 1)
        if month == 12:
            december = True
            end = date(year, month, 31)
        else: end = date(year, month + 1, 1)
        days = list() #даты в месяце
        delta = end  - start
        if delta.days<=0:
            print ("Ругаемся и выходим")
        else: 
            for i in range(delta.days + 1):
                days.append(start + timedelta(i))
            if december:
                return days
            return days[:-1] #убираем первое число след. месяца

    return "Дата введена не верно!"

def generate_year(year:int) -> list:
    '''Возвращает list() со каждтым днём в году datetime.date'''
    month = 1
    days = list()
    while month <= 12:
        start = date(year, month, 1)  # начальная дата
       
        end = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)  # конечная дата
        delta = end - start         # timedelta
        if delta.days<=0:
            print ("Ругаемся и выходим")
        value = list()
        for i in range(delta.days + 1):
            value.append(start + timedelta(i))
        days.append(value[:-1])  
        month += 1
    return days


def simple_graph(employee:str, year:int, month:int) -> dict:
    '''Возвращаем данные для графика в views.by_employee'''
    days = generate_month(year, month)
    db = ZagruzkaModel.objects.using('data').filter(Sotrudnik = employee).all()
    dates, tabel, order = [], [], []
    title = 'График рабочего времени'
    for _ in db:
         if _.Period in days:
             dates.append(_.Period.strftime("%d-%m-%Y"))
             tabel.append(_.RabVremTabel)
             order.append(_.RabVremNaryad)
    response_value = {
        'dates' : dates,
        'tabel' : tabel,
        'order' : order,
        'title' : title, 
        'year' : year,
        'month' : months[month - 1],
        'employee' : employee,
    }
             
    return response_value

def zagruzka_graph(year: int, month: int) -> dict:
    '''Возвращаем данные для графика процент загрузки для view.all_employee'''
    chached = False
    response_value = dict()
    counter = 0
    if month != 0: #если запросили месяц
        generated_month = generate_month(year, month)
        for emp in employees.values():
            counter += 1
            response_value[counter] = {}
            response_value[counter]['name'] = emp
            response_value[counter]['values'] = []
            db = ZagruzkaModel.objects.using('data').filter(Sotrudnik=emp,Period__in=generated_month).all()
            ls_from_db = list(db)
            values = {}
            for _ in ls_from_db:
                values[_.Period] = _.ProcentZagr
            for day in generated_month:
                value = values.get(day)
                response_value[counter]['values'].append(value) if value else response_value[counter]['values'].append(0)
        response_value['dates'] = generated_month
        return response_value

    if month == 0: # месяц не передали
        try:
            with open(f'data{year}.json', 'r') as f:
                response_value = json.loads(f.read())
                chached = True
            return response_value
        except FileNotFoundError:
            chached = False
        generated_year = generate_year(year)
        for emp in employees.values():
            counter += 1
            db = ZagruzkaModel.objects.using('data').filter(Sotrudnik = emp).all()
            response_value[counter] = {}
            response_value[counter]['values'] = []
            response_value[counter]['name'] = emp
            for m in generated_year:
                ls = []
                for d in m:
                    for record in db:
                        if record.Period == d:
                            ls.append(record.ProcentZagr)
                try:
                    ls = sum(ls) / len(ls)
                except ZeroDivisionError:
                    ls = 0
                response_value[counter]['values'].append(ls)
    
        response_value['dates'] = months
        if not chached:
            with open(f'data{year}.json', 'w') as f:
                f.write(json.dumps(response_value, indent=4))
        return response_value
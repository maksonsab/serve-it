from datetime import date, timedelta
from turtle import end_fill
from urllib import response

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
    "Возвращает кортеж с датами в заданном месяце"
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


def simple_graph(employee:str, year, month) -> dict:
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
    }
             
    return response_value

def zagruzka_graph(year: int, month: int):
    '''Возвращаем данные для графика процент загрузки для view.all_employee'''
    #days = generate_month(year, month)
    #db = ZagruzkaModel.objects.using('data').filter(Sotrudnik = emp).values_list('Period', 'ProcentZagr').all()
    response_value = dict()
    if month == 0:
        year = generate_year(year)
        for emp in employees.values():
            db = ZagruzkaModel.objects.using('data').filter(Sotrudnik = emp).all()
            response_value[emp] = []
            for m in year:
                ls = []
                for d in m:
                    for record in db:
                        if record.Period == d:
                            ls.append(record.ProcentZagr)
                try:
                    ls = sum(ls) / len(ls)
                except ZeroDivisionError:
                    ls = 0
                response_value[emp].append(ls)
    print(response_value)
    return response_value                            
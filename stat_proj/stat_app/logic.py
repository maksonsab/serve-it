from datetime import date, timedelta

from .models import ZagruzkaModel

months = ['Январь', 'Февраль', 'Март', "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]


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

def simple_graph(employee:str, year, month) -> dict:
    days = generate_month(year, month)
    db = ZagruzkaModel.objects.using('data').filter(Sotrudnik = employee).all()
    dates = []
    tabel = []
    title = 'График рабочего времени'
    for _ in db:
         if _.Period in days:
             dates.append(_.Period.strftime("%d-%m-%Y"))
             tabel.append(_.RabVremTabel)
    response_value = {
        'dates' : dates,
        'tabel' : tabel,
        'title' : title, 
        'year' : year,
        'month' : months[month - 1],
    }
             
    return response_value
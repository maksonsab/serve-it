from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('get_stat/', views.data_for_graph, name = 'employee_stat'),
    path('<department>', views.by_department, name = 'department_url'),
    path('<department>/<employee>', views.by_employee, name = 'employee_url'),

]
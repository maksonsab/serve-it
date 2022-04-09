from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('<otdel>', views.by_department, name = 'department_url'),
]
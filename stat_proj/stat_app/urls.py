from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('<department>', views.by_department, name = 'department_url'),

]
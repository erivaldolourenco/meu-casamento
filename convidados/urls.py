from django.urls import path

from convidados import views

urlpatterns = [
    path('presenca', views.presenca, name='presenca'),
]

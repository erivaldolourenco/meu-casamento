from django.urls import path

from convidados import views

urlpatterns = [
    path('presenca', views.presenca, name='presenca'),
    path('lista', views.lista, name='lista'),
    # path('carregar', views.carregar, name='carregar'),
]

from django.urls import path

from webpage import views

urlpatterns = [
    path(r'', views.home, name='home'),
    path(r'manutencao', views.manutencao, name='manutencao'),
]

from django.urls import path

from webpage import views

urlpatterns = [
    path(r'', views.home, name='home'),
    path(r'lista-de-presentes', views.lista_de_presentes, name='lista_de_presentes')
]
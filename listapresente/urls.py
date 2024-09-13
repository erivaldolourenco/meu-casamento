from django.urls import path

from listapresente import views

urlpatterns = [
    path('', views.lista_de_presentes, name='lista_de_presente'),
    path('<int:id_presente>/presente', views.presente, name='presente'),
    path('<int:id_presente>/pagar', views.pagar, name='pagar'),
]

from django.urls import path

from listapresente import views

urlpatterns = [
    path(r'', views.lista_de_presentes, name='lista_de_presente'),
    path(r'<id_presente>/presente', views.presente, name='presente'),
    path(r'<id_presente>/pagar', views.pagar, name='pagar'),
]

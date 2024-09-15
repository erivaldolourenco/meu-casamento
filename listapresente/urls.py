from django.urls import path

from listapresente import views

urlpatterns = [
    path('', views.lista_de_presentes, name='lista_de_presente'),
    path('<int:id_presente>/presente', views.presente, name='presente'),
    path('<int:id_presente>/pagamento', views.pagamento, name='pagamento'),
    path('pagamento-sucesso', views.pagamento_sucesso, name='pagamento_sucesso'),
    path('pagamento-erro', views.pagamento_erro, name='pagamento_erro'),
    path('pagamento-pendente', views.pagamento_pendente, name='pagamento_pendente'),
]

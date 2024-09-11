from django.urls import path

from webpage import views

urlpatterns = [
    path(r'', views.home, name='home'),
]

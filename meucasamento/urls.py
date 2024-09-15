"""
URL configuration for meucasamento project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from listapresente import views
from meucasamento import settings

urlpatterns = [
                  path('zordon/', admin.site.urls),
                  path('', include('webpage.urls')),
                  path('mercadopago', views.notificacao_mercadopago, name='notificacao_mercadopago'),
                  path('lista-de-presente/', include('listapresente.urls')),
                  path('convidados/', include('convidados.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

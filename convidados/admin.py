from django.contrib import admin

from convidados.models import Convidado, Acompanhante

class ConvidadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'presenca_confirmada')  # Exibe o nome e a presença confirmada

class AcompanhanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'convidado')

admin.site.register(Convidado, ConvidadoAdmin)
admin.site.register(Acompanhante, AcompanhanteAdmin)

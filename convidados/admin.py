from django.contrib import admin

from convidados.models import Convidado, Acompanhante, ConvidadoPresente


class ConvidadoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'presenca_confirmada')  # Exibe o nome e a presença confirmada

class AcompanhanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'convidado')

class ConvidadoPresenteAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'presente', 'preco')

admin.site.register(Convidado, ConvidadoAdmin)
admin.site.register(Acompanhante, AcompanhanteAdmin)
admin.site.register(ConvidadoPresente, ConvidadoPresenteAdmin)

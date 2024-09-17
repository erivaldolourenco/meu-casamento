from django.contrib import admin

from convidados.models import Convidado, Acompanhante, ConvidadoPresente


 # Exibe o nome e a presença confirmada

class AcompanhanteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'convidado')

class ConvidadoPresenteAdmin(admin.ModelAdmin):
    list_display = ('nome_convidado', 'sobrenome_convidado', 'email','data_compra','produto_nome','status', 'valor_recebido')

class AcompanhanteInline(admin.TabularInline):
    model = Acompanhante
    extra = 1

class ConvidadoAdmin(admin.ModelAdmin):
    inlines = [AcompanhanteInline]
    list_display = ('nome', 'presenca_confirmada', 'mesa')


admin.site.register(Convidado, ConvidadoAdmin)
admin.site.register(Acompanhante, AcompanhanteAdmin)
admin.site.register(ConvidadoPresente, ConvidadoPresenteAdmin)

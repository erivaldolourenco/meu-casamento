from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader

from alertas.telegram.telegram import enviar_telegram
from convidados.models import Convidado


# Create your views here.
def presenca(request):
    if request.method == 'POST':
        nome_convidado = request.POST.get('nome-convidado')
        template = loader.get_template("presenca.html")
        try:
            convidado = Convidado.objects.get(nome__iexact=nome_convidado)
            acompanhantes = convidado.acompanhante_set.all()
            convidado.presenca_confirmada = True
            convidado.save()
            enviar_telegram(convidado.nome + " confirmou a presença!")
        except Convidado.DoesNotExist:
            convidado = None
            acompanhantes = None
        context = {
            "convidado": convidado,
            "acompanhantes": acompanhantes,
            "nome_convidado": nome_convidado,

        }
        return HttpResponse(template.render(context, request))

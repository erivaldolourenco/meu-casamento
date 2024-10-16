from django.http import HttpResponse
from django.template import loader

from alertas.telegram.telegram import enviar_telegram
from convidados.forms import ConvidadoForm, AcompanhanteFormSet
from convidados.models import Convidado


# Create your views here.
def presenca(request):
    if request.method == 'POST':
        convidado = Convidado()
        acompanhantes = []
        form_convidado = ConvidadoForm(request.POST)
        formset_acompanhantes = AcompanhanteFormSet(request.POST)
        template = loader.get_template("presenca.html")
        try:
            if form_convidado.is_valid() and formset_acompanhantes.is_valid():
                convidado = form_convidado.save()
                formset_acompanhantes.instance = convidado
                formset_acompanhantes.save()
                acompanhantes = formset_acompanhantes.cleaned_data
                enviar_telegram(convidado.nome + " confirmou a presença!")
        except Convidado.DoesNotExist:
            convidado = None
            acompanhantes = None
        context = {
            "convidado": convidado,
            "acompanhantes": acompanhantes,

        }
        return HttpResponse(template.render(context, request))


def lista(request):
    convidados = Convidado.objects.all()
    convidados_detalhes = []
    contador_global = 1
    for convidado in convidados:
        detalhes_convidado = {
            "numero": contador_global,
            "nome": convidado.nome,
            "confirmado": "Sim" if convidado.presenca_confirmada else "Não",
            "mesa": convidado.mesa,
            "acompanhantes": [],
        }
        convidados_detalhes.append(detalhes_convidado)
        contador_global += 1
        for acompanhante in convidado.acompanhante_set.all():
            detalhes_acompanhante = {
                "numero": contador_global,
                "nome": acompanhante.nome,
            }
            detalhes_convidado["acompanhantes"].append(detalhes_acompanhante)
            contador_global += 1
    context = {
        "convidados_detalhes": convidados_detalhes,
    }
    template = loader.get_template("lista_convidados.html")
    return HttpResponse(template.render(context, request))

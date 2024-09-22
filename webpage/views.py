from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from convidados.forms import ConvidadoForm, AcompanhanteFormSet
from listapresente.models import Produto


# Create your views here.
def home(request):
    form_convidado = ConvidadoForm()
    formset_acompanhantes = AcompanhanteFormSet()

    template = loader.get_template("index.html")
    context = {
        'form_convidado': form_convidado,
        'formset_acompanhantes': formset_acompanhantes,
        "noivo": "Erivaldo",
        "noiva": "Evelyn",
        "data_casamento": "07 Dezembro",
    }
    return HttpResponse(template.render(context, request))


def manutencao(request):
    template = loader.get_template("manutencao.html")
    context = {
    }
    return HttpResponse(template.render(context, request))
